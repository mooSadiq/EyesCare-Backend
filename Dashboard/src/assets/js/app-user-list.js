import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_user_table = $('.datatables-users'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the user data,
 * and adds buttons for exporting data and adding new users.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */
function initializeDataTable(data){
  if ($.fn.DataTable.isDataTable(dt_user_table)) {
      dt_user_table.DataTable().clear().destroy();
  }
    dt_user_table.DataTable({
      data: data.users,
      columns: [
            { data: null },  // Empty column for respons
            { data: 'first_name' },
            { data: 'user_type' },
            { data: 'is_blue_verified' },
            { data: 'is_active' },
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
                var name = `${full['first_name']} ${full['last_name']}`;
                var email = full['email'];
                var image = full['profile_picture'];
                var output;
                if (image) {
                  output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
            } else {
                  var initials = `${full['first_name'][0]}${full['last_name'][0]}`;
                var stateNum = Math.floor(Math.random() * 6);
                var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                  var state = states[stateNum];
                  output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
            }
                let userId;
                let userProfileUrl;
                const userType = full['user_type'];
                if (userType === 'doctor') {
                  userId = full['doctor_id'];
                  userProfileUrl = `/doctors/profile/${userId}/`;
                  }
                else if (userType === 'patient') {
                  userId = full['patient_id'];
                  userProfileUrl = `/patients/profile/${userId}/`;
                  }
                else {                  
                  userId = full['id'];
                  userProfileUrl = `/users/profile/${userId}/`;
                  }

                return `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="avatar-wrapper">
                      <div class="avatar me-3">
                        ${output}
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="${userProfileUrl}" class="text-body text-truncate">
                        <span class="fw-medium">${name}</span>
                      </a>
                      <small class="text-muted">${email}</small>
                    </div>
                  </div>`;
              }
            },
        {
          // Render User Role
          targets: 2,
          render: function (data, type, full, meta) {
            const userType = full['user_type'];
            if (userType === 'doctor') {
              return `<span class="text-truncate d-flex align-items-center">
                            <span class="badge badge-center rounded-pill bg-label-success w-px-30 h-px-30 me-2">
                            <i class="ti ti-nurse ti-sm"></i></span>طبيب</span>`;
            }
            else if (userType === 'patient'){
              return `<span class="text-truncate d-flex align-items-center">
              <span class="badge badge-center rounded-pill bg-label-info w-px-30 h-px-30 me-2">
              <i class="ti ti-heart ti-sm"></i></span>مريض</span>`;
            }
            else if (userType === 'admin'){
              return `<span class="text-truncate d-flex align-items-center">
              <span class="badge badge-center rounded-pill bg-label-secondary w-px-30 h-px-30 me-2">
              <i class="ti ti-device-laptop ti-sm"></i></span>مدير</span>`;
            }
            else {
              return `<span class="text-truncate d-flex align-items-center">
              <span class="badge badge-center rounded-pill bg-label-warning w-px-30 h-px-30 me-2">
              <i class="ti ti-user ti-sm"></i></span>مستخدم</span>`;
            }
          }
        },
        {
        // Render user is verified with blue_verified or not
          targets: 3,
          render: function (data, type, full, meta) {
                var $ver = full['is_blue_verified'];
                if ($ver == 1) {
              return "<span class='text-truncate d-flex align-items-center'>" + '<span class="badge badge-center rounded-pill bg-label-primary w-px-30 h-px-30 me-2"><i class="ti ti-check ti-sm"></i></span>' + '<span class="fw-medium">نعم</span>' + '</span>';
              ;
            }
            else {
              return "<span class='text-truncate d-flex align-items-center'>" + '<span class="badge badge-center rounded-pill bg-label-danger w-px-30 h-px-30 me-2"><i class="ti ti-x ti-sm"></i></span>' + '<span class="fw-medium">لا</span>' + '</span>';
            }

          }
        },
        {
          // Render User Status
          targets: 4,
          render: function (data, type, full, meta) {
            var $isActive = full['is_active'];
                if ($isActive == 1) {
                  return '<span class="fw-medium badge bg-label-success text-center ">نشط</span>';
                }
                else {
                  return '<span class="fw-medium  badge bg-label-danger text-center">غير نشط</span>';
                }
          }
        },
        // Render action buttons for viewing and deleting user
        {
          targets: -1,
          title: 'Actions',
          data: null,
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
                let userId;
                let userProfileUrl;
                var userType = full['user_type'];
                if (userType === 'doctor') {
                  userId = full['doctor_id'];
                  userProfileUrl = `/doctors/profile/${userId}/`;
                  }
                else if (userType === 'patient') {
                  userId = full['patient_id'];
                  userProfileUrl = `/patients/profile/${userId}/`;
                  }
                else {                  
                  userId = full['id'];
                  userProfileUrl = `/users/profile/${userId}/`;
                  }

                return `
                  <div class="d-flex align-items-center view-profile">
                    <a href="${userProfileUrl}" class="text-body view-profile" data-id="${userId}" data-type="${userType}">
                        <i class="ti ti-eye ti-sm me-2"></i>
                    </a>
                    <a href="javascript:;" class="text-body delete-record" data-id="${userId}">
                      <i class="ti ti-trash ti-sm mx-2"></i>
                    </a>
                  </div>`;
          }
        }
      ],
      order: [[1, 'desc']],
      dom:
        '<"row me-2"' +
        '<"col-md-2"<"me-3"l>>' +
        '<"col-md-10"<"dt-action-buttons text-xl-end text-lg-start text-md-end text-start d-flex align-items-center justify-content-end flex-md-row flex-column mb-3 mb-md-0"fB>>' +
        '>t' +
        '<"row mx-2"' +
        '<"col-sm-12 col-md-6"i>' +
        '<"col-sm-12 col-md-6"p>' +
        '>',
      language: {
        sLengthMenu: '_MENU_',
        search: '',
        searchPlaceholder: 'بحث ..'
      },
      // Buttons with Dropdown
      buttons: [
        {
          extend: 'collection',
          className: 'btn btn-label-secondary dropdown-toggle mx-3 waves-effect waves-light',
          text: '<i class="ti ti-screen-share me-1 ti-xs"></i>تصدير',
          buttons: [
            {
              extend: 'print',
              text: '<i class="ti ti-printer me-2" ></i>Print',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4],
                // prevent avatar to be print
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              },
              customize: function (win) {
                //customize print view for dark
                $(win.document.body)
                  .css('color', headingColor)
                  .css('border-color', borderColor)
                  .css('background-color', bodyBg)
                  .css('direction', 'rtl');
                $(win.document.body)
                  .find('table')
                  .addClass('compact')
                  .css('color', 'inherit')
                  .css('border-color', 'inherit')
                  .css('background-color', 'inherit');
              }
            },
            {
              extend: 'csv',
              text: '<i class="ti ti-file-text me-2" ></i>Csv',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'excel',
              text: '<i class="ti ti-file-spreadsheet me-2"></i>Excel',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'pdf',
              charset: 'utf-8',
              font: 'Arial Unicode MS',
              text: '<i class="ti ti-file-code-2 me-2"></i>Pdf',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'copy',
              text: '<i class="ti ti-copy me-2" ></i>Copy',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            }
          ]
        },
        {
          text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">اضافة مستخدم جديد</span>',
          className: 'add-new btn btn-primary waves-effect waves-light',
          attr: {
            'data-bs-toggle': 'offcanvas',
            'data-bs-target': '#offcanvasAddUser'
          }
        }
      ],
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
                  return 'تفاصيل ل  ' + data['first_name'];
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      },
      initComplete: function () {
        this.api()
          .columns(2)
          .every(function () {
            var column = this;
                $('#UserRole').on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });
            });
        this.api()
          .columns(3)
          .every(function () {
            var column = this;
                $('#Userblue_verified').on('change', function () {
                    var val = $.fn.dataTable.util.escapeRegex($(this).val());
                    column.search(val ? '^' + val + '$' : '', true, false).draw();
              });
          });
        this.api()
                .columns(4)
          .every(function () {
            var column = this;
                    $('#UserStatus').on('change', function () {
                        var val = $(this).val();
                        column.search(val ? '^' + val + '$' : '', true, false).draw();
            });
                });                        
          }
    });
}

/**
 * Fetches the user data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of user data and
 * populates the DataTable with the fetched data.
 */

async function fetchAndInitializeTable() {
  const url_get_users_data = '/users/api/get/users/';
  try {
    const data = await fetchAllData(url_get_users_data);
    initializeDataTable(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات المستخدمين:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);

/**
 * Handles the submission of the 'Add New User' form.
 * This function validates the form, sends a POST request to add a new user,
 * and updates the DataTable with the newly added user.
 */
document.getElementById('addNewUserForm').addEventListener('submit', async function (event) {
  event.preventDefault();

  const formData = new FormData();
  formData.append('first_name', document.getElementById('add-user-firstname').value);
  formData.append('last_name', document.getElementById('add-user-lastname').value);
  formData.append('email', document.getElementById('add-user-email').value);
  formData.append('password', document.getElementById('formValidationPass').value);
  formData.append('user_type', document.getElementById('add-user-role').value);

  
  const method = 'POST';
  const url = '/users/api/add/';
  try {
    const result = await submitRequest(url, method, formData );
    if (result.success) {
      const offcanvasElement = document.getElementById('offcanvasAddUser');
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
    console.error('Error adding user:', error);
  }
  });


/**
 * Handles the deletion of a user when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */

$(document).on('click', '.delete-record', async function () {
    const userId = $(this).data('id');
    const result = await showConfirmationDialog();
    if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/users/api/delete/${userId}/`;
      const deleteResult = await submitRequest(url, method, null);

      if (deleteResult.success) {
        showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
        fetchAndInitializeTable();
    } else {
        showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
    }
    }
});


