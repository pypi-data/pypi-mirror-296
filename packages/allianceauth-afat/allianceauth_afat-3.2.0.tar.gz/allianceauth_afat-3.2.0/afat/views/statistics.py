"""
Statistics related views
"""

# Standard Library
import calendar
from collections import OrderedDict
from datetime import datetime

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

# Alliance Auth
from allianceauth.authentication.decorators import permissions_required
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# Alliance Auth AFAT
from afat import __title__
from afat.helper.views import (
    characters_with_permission,
    current_month_and_year,
    get_random_rgba_color,
    user_has_any_perms,
)
from afat.models import Fat
from afat.utils import get_or_create_alliance_info, get_or_create_corporation_info

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@login_required()
@permission_required(perm="afat.basic_access")
def overview(request: WSGIRequest, year: int = None) -> HttpResponse:
    """
    Statistics main view

    :param request:
    :type request:
    :param year:
    :type year:
    :return:
    :rtype:
    """

    if year is None:
        year = datetime.now().year

    user_can_see_other_corps = False

    if user_has_any_perms(
        user=request.user,
        perm_list=["afat.stats_corporation_other", "afat.manage_afat"],
    ):
        user_can_see_other_corps = True
        basic_access_permission = Permission.objects.select_related("content_type").get(
            content_type__app_label="afat", codename="basic_access"
        )

        characters_with_access = characters_with_permission(
            permission=basic_access_permission
        )

        data = {"No Alliance": [1]}
        sanity_check = {}

        # First create the alliance keys in our dict
        for character_with_access in characters_with_access:
            if character_with_access.alliance_name is not None:
                data[character_with_access.alliance_name] = [
                    character_with_access.alliance_id
                ]

        # Now append the alliance keys
        for character_with_access in characters_with_access:
            corp_id = character_with_access.corporation_id
            corp_name = character_with_access.corporation_name

            # if corp_id not in sanity_check.keys():
            if corp_id not in sanity_check:
                if character_with_access.alliance_name is None:
                    data["No Alliance"].append((corp_id, corp_name))
                else:
                    data[character_with_access.alliance_name].append(
                        (corp_id, corp_name)
                    )

            sanity_check[corp_id] = corp_id

    elif request.user.has_perm(perm="afat.stats_corporation_own"):
        data = [
            (
                request.user.profile.main_character.corporation_id,
                request.user.profile.main_character.corporation_name,
            )
        ]
    else:
        data = None

    months = _calculate_year_stats(request=request, year=year)

    context = {
        "data": data,
        "charstats": months,
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "user_can_see_other_corps": user_can_see_other_corps,
    }

    logger.info(msg=f"Statistics overview called by {request.user}")

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-overview.html",
        context=context,
    )


def _calculate_year_stats(request, year) -> list:
    """
    Calculate statistics for the year

    :param request:
    :type request:
    :param year:
    :type year:
    :return:
    :rtype:
    """

    months = []

    # Get all characters for the user and order by userprofile and character name
    characters = EveCharacter.objects.filter(
        character_ownership__user=request.user
    ).order_by("-userprofile", "character_name")

    for char in characters:
        character_fats_in_year = (
            Fat.objects.filter(fatlink__created__year=year)
            .filter(character=char)
            .values("fatlink__created__month")
            .annotate(fat_count=Count("id"))
        )

        # Only if there are FATs for this year for the character
        if character_fats_in_year:
            character_fats_per_month = {
                int(result["fatlink__created__month"]): result["fat_count"]
                for result in character_fats_in_year
            }

            # Sort by month
            character_fats_per_month = dict(
                sorted(character_fats_per_month.items(), key=lambda item: item[0])
            )

            months.append(
                (char.character_name, character_fats_per_month, char.character_id)
            )

    # Return sorted by character name
    # return sorted(months, key=lambda x: x[0])
    return months


@login_required()
@permission_required(perm="afat.basic_access")
def character(  # pylint: disable=too-many-locals
    request: WSGIRequest, charid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    Character statistics view

    :param request:
    :type request:
    :param charid:
    :type charid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    current_month, current_year = current_month_and_year()
    eve_character = EveCharacter.objects.get(character_id=charid)
    valid = [
        char.character for char in CharacterOwnership.objects.filter(user=request.user)
    ]

    can_view_character = True

    # Check if the user can view another corporation's statistics or manage AFAT
    if eve_character not in valid and not user_has_any_perms(
        user=request.user,
        perm_list=[
            "afat.stats_corporation_other",
            "afat.manage_afat",
        ],
    ):
        can_view_character = False

    # Check if the user if by any chance in the same corporation as the character
    # and can view own corporation statistics
    if (
        eve_character not in valid
        and eve_character.corporation_id
        == request.user.profile.main_character.corporation_id
        and request.user.has_perm(perm="afat.stats_corporation_own")
    ):
        can_view_character = True

    # If the user cannot view the character's statistics, send him home
    if can_view_character is False:
        messages.warning(
            request=request,
            message=mark_safe(
                s=gettext(
                    "<h4>Warning!</h4>"
                    "<p>You do not have permission to view "
                    "statistics for this character.</p>"
                )
            ),
        )

        return redirect(to="afat:dashboard")

    if not month or not year:
        messages.error(
            request=request,
            message=mark_safe(
                s=gettext("<h4>Warning!</h4><p>Date information not complete!</p>")
            ),
        )

        return redirect(to="afat:dashboard")

    fats = Fat.objects.filter(
        character__character_id=charid,
        fatlink__created__month=month,
        fatlink__created__year=year,
    )

    # Data for ship type pie chart
    data_ship_type = {}

    for fat in fats:
        if fat.shiptype in data_ship_type:
            continue

        data_ship_type[fat.shiptype] = fats.filter(shiptype=fat.shiptype).count()

    colors = []

    for _ in data_ship_type:
        bg_color_str = get_random_rgba_color()
        colors.append(bg_color_str)

    data_ship_type = [
        # Ship type can be None, so we need to convert to string here
        list(str(key) for key in data_ship_type),
        list(data_ship_type.values()),
        colors,
    ]

    # Data for by Time Line Chart
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(fatlink__created__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    context = {
        "character": eve_character,
        "month": month,
        "month_current": current_month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": current_year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_ship_type": data_ship_type,
        "data_time": data_time,
        "fats": fats,
    }

    month_name = calendar.month_name[int(month)]
    logger.info(
        msg=(
            f"Character statistics for {eve_character} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-character.html",
        context=context,
    )


@login_required()
@permissions_required(
    perm=(
        "afat.stats_corporation_other",
        "afat.stats_corporation_own",
        "afat.manage_afat",
    )
)
def corporation(  # pylint: disable=too-many-statements too-many-branches too-many-locals
    request: WSGIRequest, corpid: int = 0000, year: int = None, month: int = None
) -> HttpResponse:
    """
    Corp statistics view

    :param request:
    :type request:
    :param corpid:
    :type corpid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    if not year:
        year = datetime.now().year

    current_month, current_year = current_month_and_year()

    # Check character has permission to view other corp stats
    if int(request.user.profile.main_character.corporation_id) != int(corpid):
        if not user_has_any_perms(
            user=request.user,
            perm_list=["afat.stats_corporation_other", "afat.manage_afat"],
        ):
            messages.warning(
                request=request,
                message=mark_safe(
                    s=gettext(
                        "<h4>Warning!</h4>"
                        "<p>You do not have permission to view statistics "
                        "for that corporation.</p>"
                    )
                ),
            )

            return redirect(to="afat:dashboard")

    corp = get_or_create_corporation_info(corporation_id=corpid)
    corp_name = corp.corporation_name

    if not month:
        months = []

        for i in range(1, 13):
            corp_fats = Fat.objects.filter(
                character__corporation_id=corpid,
                fatlink__created__month=i,
                fatlink__created__year=year,
            ).count()

            avg_fats = 0
            if corp.member_count > 0:
                avg_fats = corp_fats / corp.member_count

            if corp_fats > 0:
                months.append((i, corp_fats, round(avg_fats, 2)))

        context = {
            "corporation": corp.corporation_name,
            "months": months,
            "corpid": corpid,
            "year": year,
            "year_current": current_year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 0,
        }

        return render(
            request=request,
            template_name="afat/view/statistics/statistics-corporation-year-overview.html",
            context=context,
        )

    fats = Fat.objects.filter(
        fatlink__created__month=month,
        fatlink__created__year=year,
        character__corporation_id=corpid,
    )

    characters = EveCharacter.objects.filter(corporation_id=corpid)

    # Data for Stacked Bar Graph
    # (label, color, [list of data for stack])
    data = {}

    for fat in fats:
        # if fat.shiptype in data.keys():
        if fat.shiptype in data:
            continue

        data[fat.shiptype] = {}

    chars = []

    for fat in fats:
        if fat.character.character_name in chars:
            continue

        chars.append(fat.character.character_name)

    for key, ship_type in data.items():
        for char in chars:
            ship_type[char] = 0

    for fat in fats:
        data[fat.shiptype][fat.character.character_name] += 1

    data_stacked = []

    for key, value in data.items():
        stack = []
        stack.append(key)
        stack.append(get_random_rgba_color())
        stack.append([])

        data_ = stack[2]

        for char in chars:
            data_.append(value[char])

        stack.append(data_)
        data_stacked.append(tuple(stack))

    data_stacked = [chars, data_stacked]

    # Data for By Time
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(fatlink__created__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    # Data for By Weekday
    data_weekday = []

    for i in range(1, 8):
        data_weekday.append(fats.filter(fatlink__created__iso_week_day=i).count())

    data_weekday = [
        [
            gettext("Monday"),
            gettext("Tuesday"),
            gettext("Wednesday"),
            gettext("Thursday"),
            gettext("Friday"),
            gettext("Saturday"),
            gettext("Sunday"),
        ],
        data_weekday,
        [get_random_rgba_color()],
    ]

    chars = {}

    for char in characters:
        fat_c = fats.filter(character_id=char.id).count()
        chars[char.character_name] = (fat_c, char.character_id)

    context = {
        "corp": corp,
        "corporation": corp.corporation_name,
        "month": month,
        "month_current": datetime.now().month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": datetime.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "chars": chars,
    }

    month_name = calendar.month_name[int(month)]
    logger.info(
        msg=(
            f"Corporation statistics for {corp_name} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-corporation.html",
        context=context,
    )


@login_required()
@permissions_required(perm=("afat.stats_corporation_other", "afat.manage_afat"))
def alliance(  # pylint: disable=too-many-statements too-many-branches too-many-locals
    request: WSGIRequest, allianceid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    Alliance statistics view

    :param request:
    :type request:
    :param allianceid:
    :type allianceid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    if not year:
        year = datetime.now().year

    if allianceid == "000":
        allianceid = None

    if allianceid is not None:
        ally = get_or_create_alliance_info(alliance_id=allianceid)
        alliance_name = ally.alliance_name
    else:
        ally = None
        alliance_name = "No Alliance"

    current_month, current_year = current_month_and_year()

    if not month:
        months = []

        for i in range(1, 13):
            ally_fats = Fat.objects.filter(
                character__alliance_id=allianceid,
                fatlink__created__month=i,
                fatlink__created__year=year,
            ).count()

            if ally_fats > 0:
                months.append((i, ally_fats))

        context = {
            "alliance": alliance_name,
            "months": months,
            "allianceid": allianceid,
            "year": year,
            "year_current": current_year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 1,
        }

        return render(
            request=request,
            template_name="afat/view/statistics/statistics-alliance-year-overview.html",
            context=context,
        )

    if not month or not year:
        messages.error(
            request=request,
            message=mark_safe(
                s=gettext("<h4>Error!</h4><p>Date information incomplete.</p>")
            ),
        )

        return redirect(to="afat:dashboard")

    fats = Fat.objects.filter(
        character__alliance_id=allianceid,
        fatlink__created__month=month,
        fatlink__created__year=year,
    )

    corporations = EveCorporationInfo.objects.filter(alliance=ally)

    # Data for ship type pie chart
    data_ship_type = {}

    for fat in fats:
        if fat.shiptype in data_ship_type:
            continue

        data_ship_type[fat.shiptype] = fats.filter(shiptype=fat.shiptype).count()

    colors = []

    for _ in data_ship_type:
        bg_color_str = get_random_rgba_color()
        colors.append(bg_color_str)

    data_ship_type = [
        # Ship type can be None, so we need to convert to string here
        list(str(key) for key in data_ship_type),
        list(data_ship_type.values()),
        colors,
    ]

    # Fats by corp and ship type?
    data = {}

    for fat in fats:
        if fat.shiptype in data:
            continue

        data[fat.shiptype] = {}

    corps = []

    for fat in fats:
        if fat.character.corporation_name in corps:
            continue

        corps.append(fat.character.corporation_name)

    for key, ship_type in data.items():
        for corp in corps:
            ship_type[corp] = 0

    for fat in fats:
        data[fat.shiptype][fat.character.corporation_name] += 1

    if None in data:
        data["Unknown"] = data[None]
        data.pop(None)

    data_stacked = []

    for key, value in data.items():
        stack = []
        stack.append(key)
        stack.append(get_random_rgba_color())
        stack.append([])

        data_ = stack[2]

        for corp in corps:
            data_.append(value[corp])

        stack.append(data_)
        data_stacked.append(tuple(stack))

    data_stacked = [corps, data_stacked]

    # Avg fats by corp
    data_avgs = {}

    for corp in corporations:
        c_fats = fats.filter(character__corporation_id=corp.corporation_id).count()
        avg = c_fats / corp.member_count
        data_avgs[corp.corporation_name] = round(avg, 2)

    data_avgs = OrderedDict(sorted(data_avgs.items(), key=lambda x: x[1], reverse=True))
    data_avgs = [
        list(data_avgs.keys()),
        list(data_avgs.values()),
        get_random_rgba_color(),
    ]

    # Fats by Time
    data_time = {}

    for i in range(0, 24):
        data_time[i] = fats.filter(fatlink__created__hour=i).count()

    data_time = [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]

    # Fats by weekday
    data_weekday = []

    for i in range(1, 8):
        data_weekday.append(fats.filter(fatlink__created__iso_week_day=i).count())

    data_weekday = [
        [
            gettext("Monday"),
            gettext("Tuesday"),
            gettext("Wednesday"),
            gettext("Thursday"),
            gettext("Friday"),
            gettext("Saturday"),
            gettext("Sunday"),
        ],
        data_weekday,
        [get_random_rgba_color()],
    ]

    # Corp list
    corps = {}

    for corp in corporations:
        c_fats = fats.filter(character__corporation_id=corp.corporation_id).count()
        avg = c_fats / corp.member_count
        corps[corp] = (corp.corporation_id, c_fats, round(avg, 2))

    corps = OrderedDict(sorted(corps.items(), key=lambda x: x[1][2], reverse=True))

    context = {
        "alliance": alliance_name,
        "ally": ally,
        "month": month,
        "month_current": current_month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": current_year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_avgs": data_avgs,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "corps": corps,
        "data_ship_type": data_ship_type,
    }

    month_name = calendar.month_name[int(month)]
    logger.info(
        msg=(
            f"Alliance statistics for {alliance_name} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-alliance.html",
        context=context,
    )
