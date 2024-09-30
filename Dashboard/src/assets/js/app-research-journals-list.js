
import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_journal_table = $('.datatables-journal-list'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the patient data,
 * and adds buttons for exporting data and adding new patients.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */

function initializeDataTable(data){
      if ($.fn.DataTable.isDataTable(dt_journal_table)) {
        dt_journal_table.DataTable().clear().destroy();
      }
      dt_journal_table.DataTable({
          data: data,
          columns: [
            { data: null },  // Empty column for respons
            { data: 'name' },
            { data: 'website_url' },
            { data: null }  // Actions column
          ],
          columnDefs: [
              // Control column for responsiveness
            {
              className: 'control',
              searchable: false,
              orderable: false,
              responsivePriority: 1,
              targets: 0,
              render: function (data, type, full, meta) {
                return '';
              }
            },
            {
              // Journals name and abbreviation
              targets: 1,
              responsivePriority: 2,
              render: function (data, type, full, meta) {
                var name = full['name'];
                var abbreviation = full['abbreviation'];
                var image = full['logo'];
                var output;
                if (image) {
                  output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
                } else {
                  var initials = full['name'][0];
                  var stateNum = Math.floor(Math.random() * 6);
                  var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                  var state = states[stateNum];
                  output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
                }
                return `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="avatar-wrapper">
                      <div class="avatar me-3">
                        ${output}
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="javascript:;" class="text-body text-truncate">
                        <span class="fw-medium">${abbreviation}</span>
                      </a>
                      <small class="text-muted">${name}</small>
                    </div>
                  </div>`;
              }
            },
            // Render subscription count
            {
              targets: 2,
              render: function (data, type, full, meta) {
                return `<a href="javascript:;" class="text-body">
                        ${full['website_url']}
                        </a>`;
              }
            },
            // Render action buttons for viewing and deleting journal
            {
              // Actions
              targets: -1,
              data: null,
              searchable: false,
              orderable: false,
              render: function (data, type, full, meta) {
                var journalId = full['id'];
                return `<div class="d-flex align-items-sm-center justify-content-sm-center">
                   <button class="btn btn-sm btn-icon delete-record me-2" data-id="${journalId}"><i class="ti ti-trash"></i></button>
                   <button class="btn btn-sm btn-icon edit-record" data-id="${journalId}"><i class="ti ti-edit" ></i></button>
                   </div>`;
                
              }
            },
          ],
          order: [1, 'desc'], //set any columns order asc/desc
          dom:
            '<"card-header d-flex flex-wrap pb-2"' +
            '<f>' +
            '<"d-flex justify-content-center justify-content-md-end align-items-baseline"<"dt-action-buttons d-flex justify-content-center flex-md-row mb-3 mb-md-0 ps-1 ms-1 align-items-baseline"lB>>' +
            '>t' +
            '<"row mx-2"' +
            '<"col-sm-12 col-md-6"i>' +
            '<"col-sm-12 col-md-6"p>' +
            '>',
          lengthMenu: [7, 10, 20, 50, 70, 100], //for length of menu
          language: {
            sLengthMenu: '_MENU_',
            search: '',
            searchPlaceholder: 'Search Category'
          },
          // Button for offcanvas
          buttons: [
            {
              text: '<i class="ti ti-plus ti-xs me-0 me-sm-2"></i><span class="d-none d-sm-inline-block">اضافة مجال</span>',
              className: 'add-new btn btn-primary ms-2 waves-effect waves-light',
              attr: {
                'data-bs-toggle': 'offcanvas',
                'data-bs-target': '#offcanvasJournalList'
              }
            }
          ],
          responsive: {
            details: {
              display: $.fn.dataTable.Responsive.display.modal({
                header: function (row) {
                  var data = row.data();
                  return 'تفاصيل عن ' + data.user.first_name;
                }
              }),
              type: 'column',
              renderer: function (api, rowIdx, columns) {
                var data = $.map(columns, function (col, i) {
                  return col.title !== ''
                    ? `<tr data-dt-row="${col.rowIndex}" data-dt-column="${col.columnIndex}">
                         <td>${col.title}:</td> 
                         <td>${col.data}</td>
                       </tr>`
                    : '';
                }).join('');
                return data ? $('<table class="table"><tbody />').append(data) : false;
              }
            }
          },          
        });
}

/**
 * Fetches the patient data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of patient data and
 * populates the DataTable with the fetched data.
 */
async function fetchAndInitializeTable() {
  const url_get_category_data = '/researches/journals/';
  try {
      const data = await fetchAllData(url_get_category_data);
      console.log(data);
      initializeDataTable(data.data);
  } catch (error) {
      console.error('خطأ في جلب بيانات المجلات:', error);
  }
}
// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);


/**
 * Handles the submission of the 'Add New Patient' form.
 * This function validates the form, sends a POST request to add a new patient,
 * and updates the DataTable with the newly added patient.
 */
document.getElementById('JournalAddForm').addEventListener('submit', async function (event) {
  event.preventDefault();

  const method = 'POST';
  const url = '/researches/journals/create/';
  const formData = new FormData();
  formData.append('name', document.getElementById('journal-title').value);
  formData.append('abbreviation', document.getElementById('journal-abbre').value);
  formData.append('logo', document.getElementById('journal-logo').files[0]);
  formData.append('website_url', document.getElementById('journal-url').value);

  try {
    const result = await submitRequest(url, method, formData);

    if (result.success) {
        const offcanvasElement = document.getElementById('offcanvasJournalList');
        const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
        if (offcanvas) {
            offcanvas.hide();
        }
        showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
        fetchAndInitializeTable();
        this.reset();
    } else {
      showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
    }
  } catch (error) {
    console.error('Error adding Category:', error);
  }
});


/**
 * Handles the deletion of a patient when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */
$(document).on('click', '.delete-record', async function () {
  const journalId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/researches/journals/delete/${journalId}/`;
      const deleteResult = await submitRequest(url, method);

      if (deleteResult.success) {
          showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
          fetchAndInitializeTable();
      } else {
          showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
      }
  }
});

$(document).on('click', '.edit-record', async function () {
  const journalId = $(this).data('id');
  const url = `/researches/journals/${journalId}/`;
  try {
    const journal = await fetchAllData(url);
    console.log(journal);
    // تعبئة النموذج بالبيانات المسترجعة
    $('#journal-title-edit').val(journal.data.name);
    $('#journal-abbre-edit').val(journal.data.abbreviation);
    $('#journal-url-edit').val(journal.data.website_url);
    $('#journal-id').val(journal.data.id); 

    // عرض المودال
    $('#editJournalModal').modal('show');
  } catch (error) {
      console.error('خطأ في جلب بيانات المجالات:', error);
  }
});

$('#editJournalForm').on('submit', async function(e) {
  e.preventDefault(); 
  const journalId = $('#journal-id').val();
  const formData = new FormData();
  formData.append('name', document.getElementById('journal-title-edit').value);
  formData.append('abbreviation', document.getElementById('journal-abbre-edit').value);
  formData.append('website_url', document.getElementById('journal-url-edit').value);
  // Check if a  logo is uploaded, and add it to the form data
  const upload = document.getElementById('journal-logo-edit').files[0];
  if (upload) {
      formData.append('logo', upload);
  }
  const method = 'PUT';
  const url = `/researches/journals/update/${journalId}/`;
  const updateResult = await submitRequest(url, method, formData);

  if (updateResult.success) {
      showAlert('success', 'تم التعديل!', updateResult.message, 'btn btn-success');
      fetchAndInitializeTable();
      $('#editJournalModal').modal('hide');
      $('#editJournalForm').reset();
  } else {
      showAlert('error', 'حدث خطأ!', updateResult.message, 'btn btn-danger');
  }

});

