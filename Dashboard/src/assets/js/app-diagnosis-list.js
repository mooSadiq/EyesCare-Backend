import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


/**
 * Page diagnoses List
 */

'use strict';

// الدالة الرئيسية التي يتم استعداؤها عند فتح الصفحة
$(function () {

  fetchAndInitializeTable();


});

//دالة جلب البيانات عن طريقapi
async function fetchAndInitializeTable() {
  const url_get_diagnosis_data = '/diagnosis/api/getDiagnosis/';
  try {
    const data = await fetchAllData(url_get_diagnosis_data);
    fetchDataToDatatable(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات التشخيصات:', error);
  }
}

var dt_diagnosis_table = $('.datatables-diagnoses'); //تعريف متغبر للجدول 
// دالة لأخذ البانات ووضعها داخل الجدول
function fetchDataToDatatable(data) {



  let all_diagnosis_count = 0;
  let completed_diagnosis_count = 0;
  let non_complete_diagnosis_count = 0;

  if ($.fn.DataTable.isDataTable(dt_diagnosis_table)) {
    dt_diagnosis_table.DataTable().clear().destroy();
  }

  var dt_diagnoses = dt_diagnosis_table.DataTable({
    data: data.diagnosis,
    columns: [
      { data: null },  // Empty column for responsive control
      { data: 'user.first_name' },
      { data: 'date' },
      { data: 'image' },
      { data: 'disease_name' },
      { data: 'completed' },
      { data: null }  // Actions column
    ],
    columnDefs: [
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
      {
        targets: 1,
        responsivePriority: 4,
        render: function (data, type, full, meta) {
          var name = `${full['patient'].user.first_name} ${full['patient'].user.last_name}`;
          var email = full['patient'].user.email;
          var image = full['patient'].user.profile_picture;
          var output;
          if (image) {
            output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
          } else {
            var initials = `${full['patient'].user.first_name[0]}${full['patient'].user.last_name[0]}`;
            var stateNum = Math.floor(Math.random() * 6);
            var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
            var state = states[stateNum];
            output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
          }

          var patientId = full['patient'].id;
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
      {
        // date 
        targets: 2,
        render: function (data, type, full, meta) {
          var $date = full['diagnosis_date'];
          return '<span class="fw-medium">' + $date + '</span>';
        }
      },
      {
        // diagnoses image
        targets: 3,
        searchable: false,
        orderable: false,
        render: function (data, type, full, meta) {
          var $image = full['image'];
          // For  image
          var $output = '<img src="' + $image + '" alt="diagnosis Image" class="" style="width: 100%; height: 50px; border-radius: 10px;">';
          return $output; // Return only the image
        }
      },
      {
        // diagnoses result 
        targets: 4,
        orderable: false,
        render: function (data, type, full, meta) {
          var $result = full['diagnosis_result'];
          return '<span class="fw-medium">' + $result + '</span>';
        }
      },
      {
        // status completed
        targets: 5,
        render: function (data, type, full, meta) {
          var $status = full['compeleted'];

          if ($status == true) {
            return (
              '<span class="badge bg-label-success">' +
              "مكتمل" +
              '</span>'
            );
          } else {
            return (
              '<span class="badge bg-label-danger">' +
              "لم يتم التعرف" +
              '</span>'
            );
          }
        }
      },
      {
        targets: -1,
        title: 'Actions',
        data: null,
        searchable: false,
        orderable: false,
        render: function (data, type, full, meta) {
          var diagnosisId = full['id'];
          var diagnosisReportUrl = `/diagnosis/api/report/page/${diagnosisId}/`;
          return `
            <div class="d-flex align-items-center">
              <a href="${diagnosisReportUrl}" class="text-body">
                <i class="ti ti-eye ti-sm me-2"></i>
              </a>
              <a href="javascript:;" class="text-body delete-record" data-id="${diagnosisId}">
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
                .css('background-color', bodyBg);
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
        text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">تشخيص جديد</span>',
        className: 'add-new btn btn-primary waves-effect waves-light',
        attr: {
          'data-bs-toggle': 'offcanvas',
          'data-bs-target': '#offcanvasAddDiagnose'
        }
      }
    ],
    // For responsive popup
    responsive: {
      details: {
        display: $.fn.dataTable.Responsive.display.modal({
          header: function (row) {
            var data = row.data();
            return 'Details of ' + data['full_name'];
          }
        }),
        type: 'column',
        renderer: function (api, rowIdx, columns) {
          var data = $.map(columns, function (col, i) {
            return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
              ? '<tr style="width: 100%; height: 100%;" data-dt-row="' +
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
      // Adding backage filter once table initialized
      this.api()
        .columns(5) // Assuming status is in the 5th column (index 4)
        .every(function () {
          var column = this;
          var select = $(
            '<select class="form-select" id="status-filter">' +
            '<option value="">اختر الحالة</option>' +
            '</select>'
          )
            .appendTo('.diagnoses_status')
            .on('change', function () {
              var val = $.fn.dataTable.util.escapeRegex($(this).val());
              column.search(val ? val : '', true, false).draw();
            });

          // Populate the dropdown with status options from statusObj
          var statusOptions = [
            "مكتمل",
            "لم يتم التعرف"
          ];

          for (const status of statusOptions) {
            select.append(
              '<option value="' +
              status +
              '" class="text-capitalize">' +
              status +
              '</option>'
            );
          }
        });

    }
  });


  //الجزء الخاص باعداد الاحصائيات
  $.each(data.diagnosis, function (index, diagnosis) {
    all_diagnosis_count++;

    if (diagnosis.compeleted) {
      completed_diagnosis_count++;
    } else {
      non_complete_diagnosis_count++;
    }
  });
  // حساب النسب المئوية للتشخيصات المكتملة وغير المكتملة
  let completed_percentage = 0;
  let non_complete_percentage = 0;

  if (all_diagnosis_count > 0) {
    completed_percentage = (completed_diagnosis_count / all_diagnosis_count) * 100;
    non_complete_percentage = (non_complete_diagnosis_count / all_diagnosis_count) * 100;
  }
  // تقريبهما لأقرب عدد صحيح
  completed_percentage = Math.round(completed_percentage);
  non_complete_percentage = Math.round(non_complete_percentage);

  //تضمسن الاحصائيات في العناصر
  $('#all_diagnosis_count').text(all_diagnosis_count);
  $('#completed_diagnosis_count').text(completed_diagnosis_count);
  $('#non_complete_diagnosis_count').text(non_complete_diagnosis_count);

  $('#completed_percentage').text(completed_percentage + "%");
  $('#non_complete_percentage').text(non_complete_percentage + "%");
}


// اضافة تشخيص  


document.getElementById('addNewDiagnoseForm').addEventListener('submit', async function (event) {
  // منع إرسال النموذج الافتراضي
  event.preventDefault();
  const imageInput = document.getElementById('formValidationFile');
  const formData = new FormData();
  // التحقق من وجود صورة جديدة وتحميلها إذا كانت موجودة
  if (imageInput.files[0]) {
    formData.append('image', imageInput.files[0]);
  }
  const method = 'POST';
  const url = '/diagnosis/api/add_diagnose/';


  try {
    const result = await submitRequest(url, method, formData);
if(result.success){
if (result.data.success == true) {
  const offcanvasElement = document.getElementById('offcanvasAddDiagnose');
  const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
  if (offcanvas) {
    offcanvas.hide();
  }

  // التحقق مما إذا كان disease_type غير معروف
  if (result.data.disease_type !== 'unknown') {
    showAlert('success', 'تم التشخيص!', result.message, 'btn btn-success');
    fetchAdvertisementsData();
    this.reset();
  } else {
    // إذا كان disease_type غير معروف، عرض رسالة خطأ
    showAlert('error', 'فشل التشخيص!', 'لم يتم التعرف على المرض', 'btn btn-error');
  }
} else {
  showAlert('error', 'فشل التشخيص!', result.message || 'حدث خطأ', 'btn btn-error');
}
}
  } catch (error) {
    console.error('Error adding advertisement:', error);
  }

});

//جذف تشخيص
$(document).on('click', '.delete-record', async function () {
  const diagnosis_id = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/diagnosis/api/delete/${diagnosis_id}/`;
      const deleteResult = await submitRequest(url, method);

      if (deleteResult.success) {
          showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
          fetchAndInitializeTable();
      } else {
          showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
      }
  }
});

