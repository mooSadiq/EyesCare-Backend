import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_patient_table = $('.datatables-patients'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the patient data,
 * and adds buttons for exporting data and adding new patients.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */

function initializeDataTable(data){
      if ($.fn.DataTable.isDataTable(dt_patient_table)) {
          dt_patient_table.DataTable().clear().destroy();
      }
        dt_patient_table.DataTable({
          data: data.patients,
          columns: [
            { data: null },  // Empty column for respons
            { data: 'user.first_name' },
            { data: 'subscription_count' },
            { data: 'subscription_status' },
            { data: null }  // Actions column
          ],
          columnDefs: [
              // Control column for responsiveness
            {
              className: 'control',
              searchable: false,
              orderable: false,
              responsivePriority: 2,
              targets: 0,
              render: function (data, type, full, meta) {
                return '';
              }
            },
            // Render user's name, email, and profile picture
            {
              targets: 1,
              responsivePriority: 4,
              render: function (data, type, full, meta) {
                var name = `${full['user'].first_name} ${full['user'].last_name}`;
                var email = full['user'].email;
                var image = full['user'].profile_picture;
                var output;
                if (image) {
                  output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
                } else {
                  var initials = `${full['user'].first_name[0]}${full['user'].last_name[0]}`;
                  var stateNum = Math.floor(Math.random() * 6);
                  var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                  var state = states[stateNum];
                  output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
                }

                var patientId = full['id'];
                var patientProfileUrl = `/patients/profile/${patientId}/`; 
                return `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="avatar-wrapper">
                      <div class="avatar me-3">
                        ${output}
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="${patientProfileUrl}" class="text-body text-truncate">
                        <span class="fw-medium">${name}</span>
                      </a>
                      <small class="text-muted">${email}</small>
                    </div>
                  </div>`;
              }
            },
            // Render subscription count
            {
              targets: 2,
              render: function (data, type, full, meta) {
                return `<span class="fw-medium">${full['subscription_count']}</span>`;
              }
            },
            // Render subscription status
            {
              targets: 3,
              render: function (data, type, full, meta) {
                var status = full['subscription_status'];
                if (status) {
                  return `<span class="badge bg-label-success">مشترك</span>`;
                } else {
                  return `<span class="badge bg-label-danger">غير مشترك</span>`;
                }
              }
            },
            // Render action buttons for viewing and deleting patient
            {
              targets: -1,
              title: 'Actions',
              data: null,
              searchable: false,
              orderable: false,
              render: function (data, type, full, meta) {
                var patientId = full['id'];
                var patientProfileUrl = `/patients/api/get/patient/${patientId}/`; 
                return `
                  <div class="d-flex align-items-center">
                    <a href="${patientProfileUrl}" class="text-body">
                      <i class="ti ti-eye ti-sm me-2"></i>
                    </a>
                    <a href="javascript:;" class="text-body delete-record" data-id="${patientId}">
                      <i class="ti ti-trash ti-sm mx-2"></i>
                    </a>
                  </div>`;
              }
            }
          ],
          order: [[1, 'desc']],
          dom: '<"row me-2"<"col-md-2"<"me-3"l>><"col-md-10"<"dt-action-buttons text-xl-end text-lg-start text-md-end text-start d-flex align-items-center justify-content-end flex-md-row flex-column mb-3 mb-md-0"fB>>>t<"row mx-2"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
          language: {
            sLengthMenu: '_MENU_',
            search: '',
            searchPlaceholder: 'بحث ..'
          },
          buttons: [
            {
              extend: 'collection',
              className: 'btn btn-label-secondary dropdown-toggle mx-3 waves-effect waves-light',
              text: '<i class="ti ti-screen-share me-1 ti-xs"></i>تصدير',
              buttons: [
                { extend: 'print', text: '<i class="ti ti-printer me-2"></i>Print', className: 'dropdown-item' },
                { extend: 'csv', text: '<i class="ti ti-file-text me-2"></i>Csv', className: 'dropdown-item' },
                { extend: 'excel', text: '<i class="ti ti-file-spreadsheet me-2"></i>Excel', className: 'dropdown-item' },
                { extend: 'pdf', text: '<i class="ti ti-file-code-2 me-2"></i>Pdf', className: 'dropdown-item' },
                { extend: 'copy', text: '<i class="ti ti-copy me-2"></i>Copy', className: 'dropdown-item' }
              ]
            },
            {
              text: '<span class="d-none d-sm-inline-block">اضافة مريض</span><i class="ti ti-plus ms-2 ti-xs"></i>',
              className: 'add-new btn btn-primary waves-effect waves-light',
              attr: {
                'data-bs-toggle': 'offcanvas',
                'data-bs-target': '#offcanvasAddpatient'
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
          initComplete: function () {
            this.api()
            .columns(3) 
            .every(function () {
                var column = this;
                $('#SubsStatus').on('change', function () {
                    var val = $.fn.dataTable.util.escapeRegex($(this).val());
                    column.search(val ? '^' + val + '$' : '', true, false).draw();
                });
            });                              
          }
        });

        const userSelect = document.getElementById('select-user-id');
        // Populate user select dropdown with users that are not patients
        userSelect.innerHTML = ''; // Clear existing options to avoid duplication
        data.users.forEach(user => {
          if (user.user_type !== 'patient') {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = `${user.first_name} ${user.last_name}`;
            userSelect.appendChild(option);
          }
        });
}

/**
 * Fetches the patient data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of patient data and
 * populates the DataTable with the fetched data.
 */
async function fetchAndInitializeTable() {
  const url_get_patients_data = '/patients/api/get/patients/';
  try {
      const data = await fetchAllData(url_get_patients_data);
      initializeDataTable(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات المرضى:', error);
  }
}
// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);


/**
 * Handles the submission of the 'Add New Patient' form.
 * This function validates the form, sends a POST request to add a new patient,
 * and updates the DataTable with the newly added patient.
 */
document.getElementById('addNewpatientForm').addEventListener('submit', async function (event) {
  event.preventDefault();
  const userSelect = document.getElementById('select-user-id');
  const userId = userSelect.value;

  if (!userId) {
        showAlert('error', 'فشل !', 'يرجى اختيار مستخدم لإضافته كمريض.', 'btn btn-error');
      return;
  }

  const method = 'POST';
  const url = '/patients/api/add/';
  const formData = JSON.stringify({ user_id: userId });
  try {
    const result = await submitRequest(url, method, formData, {
        headers: {
            'Content-Type': 'application/json' 
          }
    });

    if (result.success) {
        const offcanvasElement = document.getElementById('offcanvasAddpatient');
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
    console.error('Error adding patient:', error);
  }
});


/**
 * Handles the deletion of a patient when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */
$(document).on('click', '.delete-record', async function () {
  const patientId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/patients/api/delete/${patientId}/`;
      const deleteResult = await submitRequest(url, method);

      if (deleteResult.success) {
          showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
          fetchAndInitializeTable();
      } else {
          showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
      }
  }
});
