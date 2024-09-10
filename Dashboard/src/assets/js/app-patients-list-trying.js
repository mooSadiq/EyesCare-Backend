/**
 * Page User List
 */

'use strict';

// Datatable (jquery)
document.addEventListener('DOMContentLoaded', function () {
  let borderColor, bodyBg, headingColor;

  if (isDarkStyle) {
    borderColor = config.colors_dark.borderColor;
    bodyBg = config.colors_dark.bodyBg;
    headingColor = config.colors_dark.headingColor;
  } else {
    borderColor = config.colors.borderColor;
    bodyBg = config.colors.bodyBg;
    headingColor = config.colors.headingColor;
  }

  // Variable declaration for table
  const dt_user_table = document.querySelector('.datatables-users');
  const select2 = document.querySelectorAll('.select2');
  const userView = "http://127.0.0.1:8000/patients/profile";
  const statusObj = {
    1: { title: 'قيد الانتظار', class: 'bg-label-warning' },
    2: { title: 'نشط', class: 'bg-label-success' },
    3: { title: 'غير نشط', class: 'bg-label-secondary' }
  };

  if (select2.length) {
    select2.forEach(function (element) {
      const container = document.createElement('div');
      container.className = 'position-relative';
      element.parentNode.insertBefore(container, element);
      container.appendChild(element);
      $(element).select2({
        placeholder: 'Select Country',
        dropdownParent: container
      });
    });
  }

  // Users datatable
  if (dt_user_table) {
    fetch(assetsPath + 'json/patient-list.json')
      .then(response => response.json())
      .then(data => {
        console.log(data)
        const dt_user = $(dt_user_table).DataTable({
          data: data,
          columns: [
            // columns according to JSON
            { data: null},
            { data: 'full_name' },
            { data: 'diagnosis_num' },
            { data: 'consultation_num' },
            { data: 'current_plan' },
            { data: null }
          ],
          columnDefs: [
            {
              className: 'control',
              searchable: false,
              orderable: false,
              responsivePriority: 2,
              targets: 0,
              render: function (data, type, full, meta) {
                return null;
              }
            },
            {
              targets: 1,
              responsivePriority: 4,
              render: function (data, type, full, meta) {
                const $name = full['full_name'];
                const $email = full['email'];
                const $image = full['avatar'];
                let $output;

                if ($image) {
                  $output = `<img src="${assetsPath}img/avatars/${$image}" alt="Avatar" class="rounded-circle">`;
                } else {
                  const states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
                  const $state = states[Math.floor(Math.random() * 6)];
                  const $initials = $name.split(' ').map(word => word[0]).join(' ');
                  $output = `<span class="avatar-initial rounded-circle bg-label-${$state}">${$initials}</span>`;
                }

                const $row_output = `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="avatar-wrapper">
                      <div class="avatar me-3">
                        ${$output}
                      </div>
                    </div>
                    <div class="d-flex flex-column">
                      <a href="${userView}" class="text-body text-truncate"><span class="fw-medium">${$name}</span></a>
                      <small class="text-muted">${$email}</small>
                    </div>
                  </div>
                `;
                return $row_output;
              }
            },
            {
              targets: 2,
              render: function (data, type, full, meta) {
                const $dia_num = full['diagnosis_num'];
                return `<span class="fw-medium">${$dia_num}</span>`;
              }
            },
            {
              targets: 3,
              render: function (data, type, full, meta) {
                const $consult_num = full['consultation_num'];
                return `<span class="fw-medium">${$consult_num}</span>`;
              }
            },
            {
              targets: 4,
              render: function (data, type, full, meta) {
                const $status = full['current_plan'];
                let statusBadge;

                switch ($status) {
                  case "الباقة الأساسية":
                    statusBadge = '<span class="badge bg-label-warning">الباقة الأساسية</span>';
                    break;
                  case "الباقة المميزة":
                    statusBadge = '<span class="badge bg-label-success">الباقة المميزة</span>';
                    break;
                  case "الباقة القياسية":
                    statusBadge = '<span class="badge bg-label-secondary">الباقة القياسية</span>';
                    break;
                  default:
                    statusBadge = '<span class="badge bg-label-danger">غير مشترك</span>';
                }

                return statusBadge;
              }
            },
            {
              targets: -1,
              title: 'Actions',
              data: null,
              searchable: false,
              orderable: false,
              render: function (data, type, full, meta) {
                return `
                  <div class="d-flex align-items-center">
                    <a href="${userView}" class="text-body"><i class="ti ti-eye ti-sm me-2"></i></a>
                    <a href="javascript:;" class="text-body delete-record"><i class="ti ti-trash ti-sm mx-2"></i></a>
                  </div>
                `;
              }
            }
          ],
          order: [[1, 'desc']],
          dom: '<"row me-2"' +
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
                    format: {
                      body: function (inner, coldex, rowdex) {
                        if (inner.length <= 0) return inner;
                        const el = $.parseHTML(inner);
                        let result = '';
                        $.each(el, function (index, item) {
                          if (item.classList && item.classList.contains('user-name')) {
                            result += item.lastChild.firstChild.textContent;
                          } else if (item.innerText === undefined) {
                            result += item.textContent;
                          } else {
                            result += item.innerText;
                          }
                        });
                        return result;
                      }
                    }
                  },
                  customize: function (win) {
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
                    format: {
                      body: function (inner, coldex, rowdex) {
                        if (inner.length <= 0) return inner;
                        const el = $.parseHTML(inner);
                        let result = '';
                        $.each(el, function (index, item) {
                          if (item.classList && item.classList.contains('user-name')) {
                            result += item.lastChild.firstChild.textContent;
                          } else if (item.innerText === undefined) {
                            result += item.textContent;
                          } else {
                            result += item.innerText;
                          }
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
                    format: {
                      body: function (inner, coldex, rowdex) {
                        if (inner.length <= 0) return inner;
                        const el = $.parseHTML(inner);
                        let result = '';
                        $.each(el, function (index, item) {
                          if (item.classList && item.classList.contains('user-name')) {
                            result += item.lastChild.firstChild.textContent;
                          } else if (item.innerText === undefined) {
                            result += item.textContent;
                          } else {
                            result += item.innerText;
                          }
                        });
                        return result;
                      }
                    }
                  }
                }
              ]
            }
          ]
        });
      })
      .catch(error => console.error('Error loading data:', error));
  }
});
 