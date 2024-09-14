import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_consultations_table = $('.datatables-consultations'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the user data,
 * and adds buttons for exporting data and adding new users.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */
function initializeDataTable(data){

  let all_consultations_count = 0;
  let completed_consultations_count = 0;
  let non_complete_consultations_count = 0;

  if ($.fn.DataTable.isDataTable(dt_consultations_table)) {
      dt_consultations_table.DataTable().clear().destroy();
  }
    dt_consultations_table.DataTable({
      data: data.consultations,
      columns: [
            { data: null },  // Empty column for respons
            { data: 'first_name' },
            { data: 'doctor' },
            { data: 'date' },
            { data: 'is_complete' },
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
        // Render patient's name, email, and profile picture
        {
          targets: 1,
          responsivePriority: 4,
          render: function (data, type, full, meta) {
                var name = `${full['patient'].first_name} ${full['patient'].last_name}`;
                var email = full['patient'].email;
                var image = full['patient'].profile_picture;
                var output;
                if (image) {
                  output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
            } else {
                  var initials = `${full['patient'].first_name[0]}${full['patient'].last_name[0]}`;
                var stateNum = Math.floor(Math.random() * 6);
                var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                  var state = states[stateNum];
                  output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
            }
        
                var patientId = full['patient'].id;
                var patientIdProfileUrl = `/patients/profile/${patientId}/`;
                return `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="avatar-wrapper">
                      <div class="avatar me-3">
                        ${output}
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="${patientIdProfileUrl}" class="text-body text-truncate">
                        <span class="fw-medium">${name}</span>
                      </a>
                      <small class="text-muted">${email}</small>
                    </div>
                  </div>`;
              }
         },
         {
              targets: 2,
              responsivePriority: 4,
              render: function (data, type, full, meta) {
                    var name = `${full['doctor'].first_name} ${full['doctor'].last_name}`;
                    var email = full['patient'].email;
                    var image = full['doctor'].profile_picture;
                    var output;
                    if (image) {
                      output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
                } else {
                      var initials = `${full['doctor'].first_name[0]}${full['doctor'].last_name[0]}`;
                    var stateNum = Math.floor(Math.random() * 6);
                    var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                      var state = states[stateNum];
                      output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
                }
            
                    var doctorId = full['doctor'].id;
                    var doctorIdProfileUrl = `/doctors/profile/${doctorId}/`;
                    return `
                      <div class="d-flex justify-content-start align-items-center user-name">
                        <div class="avatar-wrapper">
                          <div class="avatar me-3">
                            ${output}
                          </div>
                        </div>
                        <div class="d-flex flex-column">
                          <a href="${doctorIdProfileUrl}" class="text-body text-truncate">
                            <span class="fw-medium">${name}</span>
                          </a>
                          <small class="text-muted">${email}</small>
                        </div>
                      </div>`;
                  }
         },
        {
        // Render user is verified with blue_verified or not
          targets: 3,
          render: function (data, type, full, meta) {
            var $date = full['consultation_date'];
            return '<span class="fw-medium">' + $date + '</span>';

          }
        },
        {
          // Render consultation Status
          targets: 4,
          render: function (data, type, full, meta) {
            var $isComplete = full['is_complete'];
                if ($isComplete == 1) {
                  return '<span class="fw-medium badge bg-label-success text-center ">مكتملة</span>';
                }
                else {
                  return '<span class="fw-medium  badge bg-label-danger text-center">غير مكتملة</span>';
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
                var doctorId = full['doctor'].id;
                var doctorProfileUrl = `/doctors/profile/${doctorId}/`;
                var consultationId = full['id'];
                return `
                  <div class="d-flex align-items-center view-profile">
                    <a href="${doctorProfileUrl}" class="text-body view-profile" data-id="${doctorId}">
                        <i class="ti ti-eye ti-sm me-2"></i>
                    </a>
                    <a href="javascript:;" class="text-body delete-record" data-id="${consultationId}">
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
       
      ],
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
                  return 'تفاصيل ل  ' + data['patient'].first_name;
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
                .columns(4)
          .every(function () {
            var column = this;
                    $('#consultationStatus').on('change', function () {
                        var val = $(this).val();
                        column.search(val ? '^' + val + '$' : '', true, false).draw();
            });
                });                        
          }
    });

    //الجزء الخاص باعداد الاحصائيات
  $.each(data.consultations, function (index, consultations) {
    all_consultations_count++;

    if (consultations.is_complete) {
      completed_consultations_count++;
    } else {
      non_complete_consultations_count++;
    }
  });
  // حساب النسب المئوية للاستشارات المكتملة وغير المكتملة
  let completed_percentage = 0;
  let non_complete_percentage = 0;

  if (all_consultations_count > 0) {
    completed_percentage = (completed_consultations_count / all_consultations_count) * 100;
    non_complete_percentage = (non_complete_consultations_count / all_consultations_count) * 100;
  }
  // تقريبهما لأقرب عدد صحيح
  completed_percentage = Math.round(completed_percentage);
  non_complete_percentage = Math.round(non_complete_percentage);

  //تضمسن الاحصائيات في العناصر
  $('#all_consultations_count').text(all_consultations_count);
  $('#completed_consultations_count').text(completed_consultations_count);
  $('#non_complete_consultations_count').text(non_complete_consultations_count);

  $('#completed_percentage').text(completed_percentage + "%");
  $('#non_complete_percentage').text(non_complete_percentage + "%");
}

// دالة جلب قائمة الاستشارات عبر ال api

async function fetchAndInitializeTable() {
  const url_get_users_data = '/consultations/api/getConsultations/';
  try {
    const data = await fetchAllData(url_get_users_data);
    initializeDataTable(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات التشخيصات:', error);
  }
}

// الدالة التي تعمل فور استدعاء الصفحة
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);



//دالة حذف تشخيص

$(document).on('click', '.delete-record', async function () {
    const consultationId = $(this).data('id');
    const result = await showConfirmationDialog();
    if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/consultations/api/delete/${consultationId}/`;
      const deleteResult = await submitRequest(url, method, null);

      if (deleteResult.success) {
        showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
        fetchAndInitializeTable();
    } else {
        showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
    }
    }
});


