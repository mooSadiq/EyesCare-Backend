import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';
// Variable declaration for table
var dt_diseases_table = $('.datatables-diseases');
/**
 * Initializes the DataTable with the provided data.
 * This function configures the table columns, renders the patient data,
 * and adds buttons for exporting data and adding new Deasease.
 * It also ensures the table is responsive and sets up filtering for subscription status.
 */


function initializeDataTable(data){
  if($.fn.DataTable.isDataTable(dt_diseases_table)){
    dt_diseases_table.DataTable().clear().destroy();
  }
  dt_diseases_table.DataTable({
    data:data.Diseases,
    columns:[
      {data:null},
      {data:'name'},
      {data:'image'},
      {data:'status'},
      {data:'created_at'},
      {data:null},
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
      targets: 1,
              responsivePriority: 4,
              render: function (data, type, full, meta) {
                var name=full.name;
                var diseaseId = full.id;
                var diseaseProfileUrl = `/diseases/details/${diseaseId}/`; 
                return `
                  <div class="d-flex justify-content-start align-items-center user-name">
                    <div class="d-flex flex-column">
                      <a href="${diseaseProfileUrl}" class="text-body text-truncate">
                        <span class="fw-medium">${name}</span>
                      </a>
                    </div>
                  </div>`;
              }
  },
  {
    targets:2,
    render:function(data,type,full,meta){
      var image=full.image;
      var output;
      if(image){
        output = `<img src= "${image}" alt="disease Image" class="" style="width: 100%; height: 50px; border-radius: 10px;">`;
      }
      else{
        var initials = `${full['name'][0]}`;
        var stateNum = Math.floor(Math.random() * 6);
        var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
        var state = states[stateNum];
        output = `<div class="avatar-wrapper">
        <div class="avatar me-3">
        <span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>
        </div>
      </div>`
      }
      return output;
    }
  },
  {
    targets: 3,
    render: function (data, type, full, meta) {
      var status = full.status;
      if(status='متاحاً للتشخيص')
        return `<span class="badge bg-label-success">${status}</span>`;
      else
        return `<span class="badge bg-label-danger">${status}</span>`;
      }
  },
  {
    targets: 4,
    orderable: false,
    render: function (data, type, full, meta) {
      var $date_of_adding = full.created_at;
      return '<span class="fw-medium">' + $date_of_adding + '</span>';
      }
  },
  {
    targets: -1,
              title: 'Actions',
              data: null,
              searchable: false,
              orderable: false,
              render: function (data, type, full, meta) {
                var diseaseId=full.id;
                var diseaseProfileUrl=`/diseases/details/${diseaseId}/`;
                return `
                <div class="d-flex align-items-center">
                  <a href="${diseaseProfileUrl}" class="text-body">
                    <i class="ti ti-eye ti-sm me-2"></i>
                  </a>
                  <a href="javascript:;" class="text-body delete-record" data-id="${diseaseId}">
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
      text: '<span class="d-none d-sm-inline-block">اضافة مرض</span><i class="ti ti-plus ms-2 ti-xs"></i>',
        className: 'add-new btn btn-primary waves-effect waves-light',
        attr: {
          'data-bs-toggle': 'offcanvas',
          'data-bs-target': '#offcanvasAdddiseases'
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
    // Adding backage filter once table initialized
    this.api()
    .columns(6) // Assuming status is in the 5th column (index 4)
    .every(function () {
      var column = this;
      var select = $(
        '<select class="form-select" id="status-filter">' +
          '<option value="">اختر الحالة</option>' +
        '</select>'
      )
      .appendTo('.diseases_status')
      .on('change', function () {
        var val = $.fn.dataTable.util.escapeRegex($(this).val());
        column.search(val ? val : '', true, false).draw(); 
      });
      var statusOptions = [
        "متاح للتشخيص",
        "ليس متاحاً للتشخيص"
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
}

/**
 * Fetches the diseases data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of diseases data and
 * populates the DataTable with the fetched data.
 */
async function fetchAndInitializeTable() {
  const url_get_deseases_data = '/disease/api/get/diseases/';
  try {
      const data = await fetchAllData(url_get_deseases_data);
      initializeDataTable(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات الأمراض:', error);
  }
}
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);


/**
 * Handles the submission of the 'Add New Diseases' form.
 * This function validates the form, sends a POST request to add a new Diseases,
 * and updates the DataTable with the newly added Diseases.
 */
document.getElementById('diseaseForm').addEventListener('submit', async function (event) {
  event.preventDefault();
  const method = 'POST';
  const url = '/diseases/api/set/disease/';
  try {
    const result = await submitRequest(url, method, formData, {
        headers: {
            'Content-Type': 'application/json' 
          }
    })
    if (result.success) {
      const offcanvasElement = document.getElementById('offcanvasAdddiseases');
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
 * Handles the deletion of a Deases when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */
$(document).on('click', '.delete-record', async function () {
  const diseaseId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/diseases/api/delate/disease/${diseaseId}/`;
      const deleteResult = await submitRequest(url, method);
      if (deleteResult.success) {
          showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
          fetchAndInitializeTable();
      } else {
          showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
      }
  }
});