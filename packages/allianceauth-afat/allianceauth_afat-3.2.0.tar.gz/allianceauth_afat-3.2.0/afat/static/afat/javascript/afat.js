/**
 * Datetime format for AFAT
 *
 * @type {string}
 */
const AFAT_DATETIME_FORMAT = 'YYYY-MMM-DD, HH:mm'; // eslint-disable-line no-unused-vars

/**
 * Convert a string to a slug
 * @param {string} text
 * @returns {string}
 */
const convertStringToSlug = (text) => { // eslint-disable-line no-unused-vars
    'use strict';

    return text.toLowerCase()
        .replace(/[^\w ]+/g, '')
        .replace(/ +/g, '-');
};

/**
 * Sorting a table by its first columns alphabetically
 * @param {element} table
 * @param {string} order
 */
const sortTable = (table, order) => { // eslint-disable-line no-unused-vars
    'use strict';

    const asc = order === 'asc';
    const tbody = table.find('tbody');

    tbody.find('tr').sort((a, b) => {
        if (asc) {
            return $('td:first', a).text().localeCompare($('td:first', b).text());
        } else {
            return $('td:first', b).text().localeCompare($('td:first', a).text());
        }
    }).appendTo(tbody);
};

/**
 * Manage a modal window
 * @param {element} modalElement
 */
const manageModal = (modalElement) => { // eslint-disable-line no-unused-vars
    'use strict';

    modalElement.on('show.bs.modal', (event) => {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const url = button.data('url'); // Extract info from data-* attributes
        const cancelText = button.data('cancel-text');
        const confirmText = button.data('confirm-text');
        const bodyText = button.data('body-text');
        let cancelButtonText = modalElement.find('#cancelButtonDefaultText').text();
        let confirmButtonText = modalElement.find('#confirmButtonDefaultText').text();

        if (typeof cancelText !== 'undefined' && cancelText !== '') {
            cancelButtonText = cancelText;
        }

        if (typeof confirmText !== 'undefined' && confirmText !== '') {
            confirmButtonText = confirmText;
        }

        modalElement.find('#cancel-action').text(cancelButtonText);
        modalElement.find('#confirm-action').text(confirmButtonText);

        modalElement.find('#confirm-action').attr('href', url);
        modalElement.find('.modal-body').html(bodyText);
    }).on('hide.bs.modal', () => {
        modalElement.find('.modal-body').html('');
        modalElement.find('#cancel-action').html('');
        modalElement.find('#confirm-action').html('');
        modalElement.find('#confirm-action').attr('href', '');
    });
};

/**
 * Prevent double form submits
 */
document.querySelectorAll('form').forEach((form) => {
    'use strict';

    form.addEventListener('submit', (e) => {
        // Prevent if already submitting
        if (form.classList.contains('is-submitting')) {
            e.preventDefault();
        }

        // Add class to hook our visual indicator on
        form.classList.add('is-submitting');
    });
});
