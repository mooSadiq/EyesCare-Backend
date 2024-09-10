
import { fetchAllData, submitRequest } from './api.js';
import {showAlert, showConfirmationDialog } from './general-function.js'
'use strict';
var dt_reviews_table=$('.datatables-review')


function initializeDataTable(data){
  if($.fn.DataTable.isDataTable(dt_reviews_table)){
    dt_reviews_table.DataTable().clear().destroy();
  }
  dt_reviews_table.DataTable({
    data:data.Reviews,
    columns:[
      {data:null},
      {data:'first_name'},
      {data:'rating'},
      {data:'comment'},
      {data:'created_at'},
      {data:null}
    ],
    columnDefs:[
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

          var userId = full['user_id'];
          var userProfileUrl = `/users/profile/${userId}/`; 
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
        targets:2,
        render:function(data,type,full,meta){
          return `<span class="fw-medium">${full['rating']}</span>`
        }
      },
      {
        targets:3,
        render:function(data,type,full,meta){
          return `<span class="fw-medium">${full['comment']}</span>`
        }
      },
      {
        targets:4,
        render:function(data,type,full,meta){
          return `<span class="fw-medium">${full['created_at']}</span>`
        }
      },
      {
        targets: -1,
        title: 'Actions',
        data: null,
        searchable: false,
        orderable: false,
        render: function (data, type, full, meta) {
          var reviewId=full['id'];
          return `
          <div class="d-flex align-items-center">
          <a href="javascript:;" class="text-body delete-record" data-id="${reviewId}">
          <i class="ti ti-trash ti-sm mx-2"></i>
          </a>
          </div>`
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
async function fetchAndInitializeTable() {
  const url_get_reviews_data = '/evaluations/api/getreviews/';
  try {
      const data = await fetchAllData(url_get_reviews_data);
      console.log(data);
      initializeDataTable(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات التقيمات:', error);
  }
}
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);


$(document).on('click', '.delete-record', async function () {
  const reviewtId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
      const method = 'DELETE';
      const url = `/evaluations/api/deletereview/${reviewtId}/`;
      const deleteResult = await submitRequest(url, method);
      if (deleteResult.success) {
          showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
          fetchAndInitializeTable();
      } else {
          showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
      }
  }
});