import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_research_table = $('.datatables-research'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the user data,
 * and adds buttons for exporting data and adding new users.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */
function initializeDataTable(data){
  if ($.fn.DataTable.isDataTable(dt_research_table)) {
      dt_research_table.DataTable().clear().destroy();
  }
    dt_research_table.DataTable({
      data: data.research,
      columns: [
            { data: null },  // Empty column for respons
            { data: 'title' },
            { data: 'institution' },
            { data: 'is_file' },
            { data: 'publicate_date' },
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
        // Render research's name, email, and profile picture
        {
          targets: 1,
          responsivePriority: 2,
          render: function (data, type, full, meta) {
                var title = full['title'];
                var journal = full['journal'];
                var field_name = full['field_name'];
                return `
                    <div class="d-flex flex-column">
                      <span class="my-1 text-body text-wrap">${title}</span>
                      <div class="d-flex justify-content-start  align-items-center">
                        <small class="text-muted">${journal}</small>
                        <span class="fw-medium badge bg-label-success text-center me-2 ms-4 ">${field_name}</span>
                      </div>
                    </div>`;
              }
            },
        {
          // Render research type
          targets: 2,
          render: function (data, type, full, meta) {
            var institution = full['institution'];
            return `<span class="fw-medium">${institution}</span>`;
          }
        },
        {
          // Render User Status
          targets: 3,
          render: function (data, type, full, meta) {
            var isFile = full['is_file'];
                if (isFile) {
                  return '<span class="fw-medium  badge bg-label-danger text-center">PDF</span>';
                }
                else {
                  return '<span class="fw-medium badge bg-label-success text-center ">URL</span>';
                }
          }
        },        
        {
          // Render research type
          targets: 4,
          render: function (data, type, full, meta) {
            var publicate_date = full['publication_date'];
            return `<span class="fw-medium">${publicate_date}</span>`;
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
                var researchId = full['id'];
                var researchUrl = `/researches/details/${researchId}/`;
                return `
                  <div class="d-flex align-items-center view-profile">
                    <a href="${researchUrl}" class="text-body view-profile" data-id="${researchId}">
                        <i class="ti ti-eye ti-sm me-2"></i>
                    </a>
                    <a href="javascript:;" class="text-body delete-record" data-id="${researchId}">
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
          text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">اضافة دراسة جديد</span>',
          className: 'add-new btn btn-primary waves-effect waves-light',
          attr: {
            'data-bs-toggle': 'offcanvas',
            'data-bs-target': '#offcanvasAddResearch'
          }
        }
      ],
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
                  return 'تفاصيل الدراسة  ';
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

    const journalFormSelect = document.getElementById('add-research-select-journal');
    const journalSelect = document.getElementById('filter-jornal-select');

    initializeSelectData(data.journal, journalFormSelect);
    initializeSelectData(data.journal, journalSelect);
    // Populate user select dropdown with users that are not patients

    const fieldFormSelect = document.getElementById('add-research-select-field');
    const fieldSelect = document.getElementById('filter-field-select');
    initializeSelectData(data.field, fieldFormSelect);
    initializeSelectData(data.field, fieldSelect);

}

function initializeSelectData(data, element){
  element.innerHTML = ''; // Clear existing options to avoid duplication
  
  data.forEach(field => {
      const option = document.createElement('option');
      option.value = field.id;
      option.textContent = field.name;
      element.appendChild(option);      
  });
}


function showResearchStatistics(data) {

  document.getElementById('research-count').innerText = data.research_count;
  document.getElementById('pdf-count').innerText = data.pdf_count;
  document.getElementById('no_pdf-count').innerText = data.no_pdf_count;
  document.getElementById('journal-count').innerText = data.journal_count;
  document.getElementById('field-count').innerText = data.field_count;
  document.getElementById('total-downloads').innerText = data.total_downloads;
  
}

/**
 * Fetches the user data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of user data and
 * populates the DataTable with the fetched data.
 */

async function fetchAndInitializeTable() {
  const url_get_researrch_data = '/researches/list/';
  const url_get_Statistics_data = '/researches/list/statistics/';
  try {
    const data = await fetchAllData(url_get_researrch_data);
    const statistics = await fetchAllData(url_get_Statistics_data);
    initializeDataTable(data);
    console.log(statistics.data);
    showResearchStatistics(statistics.data);
    console.log(statistics.data);
  } catch (error) {
    console.error('خطأ في جلب البيانات :', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() { 
  fetchAndInitializeTable();

  var switchInput = document.getElementById('add-research-switch');
  const is_file = document.getElementById('add-research-switch').checked ? '1' : '0';
  console.log(is_file);
  var fileField = document.getElementById('file-input');
  fileField.style.display = 'none';
  switchInput.addEventListener('change', function() {
    var fileField = document.getElementById('file-input');
    var urlField = document.getElementById('url-input');

    if (switchInput.checked) {
      fileField.style.display = 'block';  // Show the file input
      urlField.style.display = 'none';    // Hide the URL input
    } else {
      fileField.style.display = 'none';   // Hide the file input
      urlField.style.display = 'block';   // Show the URL input
    }
  });
});

/**
 * Handles the submission of the 'Add New User' form.
 * This function validates the form, sends a POST request to add a new user,
 * and updates the DataTable with the newly added user.
 */
document.getElementById('addNewResearchForm').addEventListener('submit', async function (event) {
  event.preventDefault();

  const formData = new FormData();
  formData.append('title', document.getElementById('add-research-title').value);
  formData.append('abstract', document.getElementById('add-research-abstract').value);
  formData.append('authors', document.getElementById('add-research-authors').value);
  formData.append('publication_date', document.getElementById('add-research-date').value);
  formData.append('journal', document.getElementById('add-research-select-journal').value);
  formData.append('field', document.getElementById('add-research-select-field').value);
  formData.append('institution', document.getElementById('add-research-institution').value);
  const is_file = document.getElementById('add-research-switch').checked;  
  formData.append('is_file', is_file ? '1' : '0');
  if(is_file) {
    const upload = document.getElementById('add-research-file').files[0];
    if (upload) {
      formData.append('file', upload);
    }
  }
  else {
    formData.append('url', document.getElementById('add-research-url').value);
  }

  
  const method = 'POST';
  const url = '/researches/create/';
  try {
    const result = await submitRequest(url, method, formData );
    if (result.success) {
      const offcanvasElement = document.getElementById('offcanvasAddResearch');
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

  document.getElementById('addJournalForm').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const method = 'POST';
    const url = '/researches/journals/create/';
    const formData = new FormData();
    formData.append('name', document.getElementById('add-journal-title').value);
    formData.append('abbreviation', document.getElementById('add-journal-abbre').value);
    formData.append('logo', document.getElementById('add-journal-logo').files[0]);
    formData.append('website_url', document.getElementById('add-journal-url').value);
  
    try {
      const result = await submitRequest(url, method, formData);
  
      if (result.success) {
          const modalElement = document.getElementById('addJournalModal');
          const offcanvas = bootstrap.Modal.getInstance(modalElement);
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
 * Handles the deletion of a user when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */

$(document).on('click', '.delete-record', async function () {
    const researchId = $(this).data('id');
    const result = await showConfirmationDialog();
    if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/researches/list/${researchId}/`;
      const deleteResult = await submitRequest(url, method, null);

      if (deleteResult.success) {
        showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
        fetchAndInitializeTable();
    } else {
        showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
    }
    }
});


