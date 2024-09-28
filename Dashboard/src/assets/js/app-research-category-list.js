
import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
var dt_category_table = $('.datatables-category-list'); 

/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the patient data,
 * and adds buttons for exporting data and adding new patients.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */

function initializeDataTable(data){
      if ($.fn.DataTable.isDataTable(dt_category_table)) {
        dt_category_table.DataTable().clear().destroy();
      }
      dt_category_table.DataTable({
          data: data,
          columns: [
            { data: null },  // Empty column for respons
            { data: 'name' },
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
            {
              // Categories and Category Detail
              targets: 1,
              responsivePriority: 2,
              render: function (data, type, full, meta) {
                var $name = full['name'],
                  $category_detail = full['description'],
                  $id = full['id'];
                // Creates full output for Categories and Category Detail
                var $row_output =
                  '<div class="d-flex flex-column justify-content-center" style="width: 90%;">' +
                  '<span class="text-body text-wrap fw-medium">' +
                  $name +
                  '</span>' +
                  '<span class="text-muted text-wrap mb-0 d-none d-sm-block"><small>' +
                  $category_detail +
                  '</small></span>' +
                  '</div>';
                return $row_output;
              }
            },
            // Render action buttons for viewing and deleting Category
            {
              // Actions
              targets: -1,
              data: null,
              searchable: false,
              orderable: false,
              render: function (data, type, full, meta) {
                var categoryId = full['id'];
                return
                  `<div class="d-flex align-items-sm-center justify-content-sm-center">
                   <button class="btn btn-sm btn-icon delete-record me-2" data-id="${categoryId}"><i class="ti ti-trash"></i></button>
                   <button class="btn btn-sm btn-icon edit-record" data-id="${categoryId}"><i class="ti ti-edit" ></i></button>
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
                'data-bs-target': '#offcanvasCategoryList'
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
  const url_get_category_data = '/api/researches/fields/';
  try {
      const data = await fetchAllData(url_get_category_data);
      console.log(data);
      initializeDataTable(data.data);
  } catch (error) {
      console.error('خطأ في جلب بيانات المجالات:', error);
  }
}
// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);


/**
 * Handles the submission of the 'Add New Patient' form.
 * This function validates the form, sends a POST request to add a new patient,
 * and updates the DataTable with the newly added patient.
 */
document.getElementById('categoryListForm').addEventListener('submit', async function (event) {
  event.preventDefault();

  const method = 'POST';
  const url = '/researches/fields/create/';
  const formData = new FormData();
  formData.append('name', document.getElementById('category-title').value);
  formData.append('description', document.getElementById('category-description').value);

  try {
    const result = await submitRequest(url, method, formData);

    if (result.success) {
        const offcanvasElement = document.getElementById('offcanvasCategoryList');
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
  const categoryId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/researches/fields/delete/${categoryId}/`;
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
  const categoryId = $(this).data('id');
  const url = `/researches/fields/${categoryId}/`;
  try {
    const category = await fetchAllData(url);
    console.log(category);
    // تعبئة النموذج بالبيانات المسترجعة
    $('#category-title-edit').val(category.data.name);
    $('#category-description-edit').val(category.data.description);
    $('#category-id').val(category.data.id); 

    // عرض المودال
    $('#editCategory').modal('show');
  } catch (error) {
      console.error('خطأ في جلب بيانات المجالات:', error);
  }
});

$('#editCategoryForm').on('submit', async function(e) {
  e.preventDefault(); 
  const categoryId = $('#category-id').val();
  const formData = new FormData();
  formData.append('name', document.getElementById('category-title-edit').value);
  formData.append('description', document.getElementById('category-description-edit').value);
  console.log(formData)
  const method = 'PUT';
  const url = `/researches/fields/${categoryId}/`;
  const updateResult = await submitRequest(url, method, formData);

  if (updateResult.success) {
      showAlert('success', 'تم التعديل!', updateResult.message, 'btn btn-success');
      fetchAndInitializeTable();
      $('#editCategory').modal('hide');
  } else {
      showAlert('error', 'حدث خطأ!', updateResult.message, 'btn btn-danger');
  }

});

