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
                var diseaseProfileUrl = `/diseases/api/get/diseasebyid/${diseaseId}/`; 
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
                var diseaseProfileUrl=`/diseases/api/get/diseasebyid/${diseaseId}/`;
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
 * Fetches the deseases data from the server and initializes the DataTable.
 * This function handles asynchronous fetching of deseases data and
 * populates the DataTable with the fetched data.
 */
async function fetchAndInitializeTable() {
  const url_get_deseases_data = '/diseases/api/get/diseases/';
  try {
      const data = await fetchAllData(url_get_deseases_data);
      initializeDataTable(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات الأمراض:', error);
  }
}
document.addEventListener('DOMContentLoaded', fetchAndInitializeTable);



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


// //   // Delete Record
// //   $('.datatables-diseases tbody').on('click', '.delete-record', function () {
// //     dt_diseases.row($(this).parents('tr')).remove().draw();
// //   });

// //   // Filter form control to default size
// //   // ? setTimeout used for multilingual table initialization
// //   setTimeout(() => {
// //     $('.dataTables_filter .form-control').removeClass('form-control-sm');
// //     $('.dataTables_length .form-select').removeClass('form-select-sm');
// //   }, 300);


// // // Validation & Phone mask
// // (function () {
// //   const phoneMaskList = document.querySelectorAll('.phone-mask'),
// //     addNewUserForm = document.getElementById('addNewUserForm');

// //   // Phone Number
// //   if (phoneMaskList) {
// //     phoneMaskList.forEach(function (phoneMask) {
// //       new Cleave(phoneMask, {
// //         phone: true,
// //         phoneRegionCode: 'US'
// //       });
// //     });
// //   }
// //   // Add New User Form Validation
// //   const fv = FormValidation.formValidation(addNewUserForm, {
// //     fields: {
// //       userFullname: {
// //         validators: {
// //           notEmpty: {
// //             message: 'Please enter fullname '
// //           }
// //         }
// //       },
// //       userEmail: {
// //         validators: {
// //           notEmpty: {
// //             message: 'Please enter your email'
// //           },
// //           emailAddress: {
// //             message: 'The value is not a valid email address'
// //           }
// //         }
// //       }
// //     },
// //     plugins: {
// //       trigger: new FormValidation.plugins.Trigger(),
// //       bootstrap5: new FormValidation.plugins.Bootstrap5({
// //         // Use this for enabling/changing valid/invalid class
// //         eleValidClass: '',
// //         rowSelector: function (field, ele) {
// //           // field is the field name & ele is the field element
// //           return '.mb-3';
// //         }
// //       }),
// //       submitButton: new FormValidation.plugins.SubmitButton(),
// //       // Submit the form when all fields are valid
// //       // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
// //       autoFocus: new FormValidation.plugins.AutoFocus()
// //     }
// //   });
// // })();

// function getDiseasesData(){
//   fetch('/diseases/api/getdiseases/')
//   .then((response)=>{
//     if(!response.ok){
//       throw new Error('Response was not ok ' + response.statusText);
//     }
//     return response.json();
//   })
//   .then((data)=>{
//     if ($.fn.DataTable.isDataTable(dt_diseases_table)) {
//       dt_diseases_table.DataTable().clear().destroy();
//   }
// // diseases datatable
//   var dt_diseases = dt_diseases_table.DataTable({
//     data: data.Diseases,
//     columns: [
//       // columns according to JSON
//       { data: null },
//       { data: 'name' },
//       { data: null }
//       // { data: 'status' },
//       // { data: 'diagnosis_number' },
//       // { data: 'date_of_adding' },

//     ],
//     columnDefs: [
//       {
//         // For Responsive
//         className: 'control',
//         searchable: false,
//         orderable: false,
//         responsivePriority: 2,
//         targets: 0,
//         render: function (data, type, full, meta) {
//           return '';
//         }
//       },
//       {
//         // Disease Name
//         targets: 1,
//         responsivePriority: 4,
//         render: function (data, type, full, meta) {
//           var $name = full['name']
//           if ($image) {
//             // For Avatar image
//             var $output =
//               '<img src="' + assetsPath + 'img/avatars/' + $image + '" alt="Avatar" class="rounded-circle">';
//           } else {
//             // For Avatar badge
//             var stateNum = Math.floor(Math.random() * 6);
//             var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
//             var $state = states[stateNum],
//               $name = full['name'],
//             $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $name + '</span>';
//           }
//           // Creates full output for row
//           // var $row_output =
//           //   '<div class="d-flex justify-content-start align-items-center user-name">' +
//           //   '<div class="avatar-wrapper">' +
//           //   '<div class="avatar me-3">' +
//           //   $output +
//           //   '</div>' +
//           //   '</div>' +
//           //   '<div class="d-flex flex-column">' +
//           //   '<a href="' +
//           //   userView +
//           //   '" class="text-body text-truncate"><span class="fw-medium">' +
//           //   $name +
//           //   '</span></a>' +
          
//           //   '</div>' +
//           //   '</div>';
//           return $output;
//         }
//       },
//       // {
//       //   // status
//       //   targets: 2,
//       //   render: function (data, type, full, meta) {
//       //     var $status = full['status'];
        
//       //     if ($status === 1) {
//       //       return (
//       //         '<span class="badge bg-label-success">' +
//       //         "متاح للتشخيص" +
//       //         '</span>'
//       //       );
//       //     } else {
//       //       return (
//       //         '<span class="badge bg-label-danger">' +
//       //         "  ليس متاحاً للتشخيص" +
//       //         '</span>'
//       //       );
//       //     }
//       //   }
//       // },
//       // {
//       //   // diseases number
//       //   targets: 3,
//       //   searchable: false,
//       //   orderable: false,
//       //   render: function (data, type, full, meta) {
//       //     var $diagnosis_number = full['diagnosis_number'];
//       //     // For  count
//       //     var $output = '<span class="fw-medium">' + $diagnosis_number + '</span>';
//       //     return $output; // Return only the count
//       //   }
//       // },
//       // {
//       //   // date of adding
//       //   targets: 4,
//       //   orderable: false,
//       //   render: function (data, type, full, meta) {
//       //     var $date_of_adding = full['date_of_adding'];
//       //     return '<span class="fw-medium">' + $date_of_adding + '</span>';
//       //   }
//       // },
    
//       {
//         // Actions
//         targets: -1,
//         title: 'Actions',
//         data: null,
//         searchable: false,
//         orderable: false,
//         render: function (data, type, full, meta) {
//           return (
//             '<div class="d-flex align-items-center">' +
//             '<a href="' +
//             diseasesView +
//             '" class="text-body"><i class="ti ti-eye ti-sm me-2"></i></a>' +
//             '<a href="javascript:;" class="text-body delete-record"><i class="ti ti-trash ti-sm mx-2"></i></a>' +
//             '</div>'
//           );
//         }
//       }
//     ],
//     order: [[1, 'desc']],
//     dom:
//       '<"row me-2"' +
//       '<"col-md-2"<"me-3"l>>' +
//       '<"col-md-10"<"dt-action-buttons text-xl-end text-lg-start text-md-end text-start d-flex align-items-center justify-content-end flex-md-row flex-column mb-3 mb-md-0"fB>>' +
//       '>t' +
//       '<"row mx-2"' +
//       '<"col-sm-12 col-md-6"i>' +
//       '<"col-sm-12 col-md-6"p>' +
//       '>',
//     language: {
//       sLengthMenu: '_MENU_',
//       search: '',
//       searchPlaceholder: 'بحث ..'
//     },
//     // Buttons with Dropdown
//     buttons: [
//       {
//         extend: 'collection',
//         className: 'btn btn-label-secondary dropdown-toggle mx-3 waves-effect waves-light',
//         text: '<i class="ti ti-screen-share me-1 ti-xs"></i>تصدير',
//         buttons: [
//           {
//             extend: 'print',
//             text: '<i class="ti ti-printer me-2" ></i>Print',
//             className: 'dropdown-item',
//             exportOptions: {
//               columns: [1, 2, 3, 4],
//               // prevent avatar to be print
//               format: {
//                 body: function (inner, coldex, rowdex) {
//                   if (inner.length <= 0) return inner;
//                   var el = $.parseHTML(inner);
//                   var result = '';
//                   $.each(el, function (index, item) {
//                     if (item.classList !== undefined && item.classList.contains('user-name')) {
//                       result = result + item.lastChild.firstChild.textContent;
//                     } else if (item.innerText === undefined) {
//                       result = result + item.textContent;
//                     } else result = result + item.innerText;
//                   });
//                   return result;
//                 }
//               }
//             },
//             customize: function (win) {
//               //customize print view for dark
//               $(win.document.body)
//                 .css('color', headingColor)
//                 .css('border-color', borderColor)
//                 .css('background-color', bodyBg);
//               $(win.document.body)
//                 .find('table')
//                 .addClass('compact')
//                 .css('color', 'inherit')
//                 .css('border-color', 'inherit')
//                 .css('background-color', 'inherit');
//             }
//           },
//           {
//             extend: 'csv',
//             text: '<i class="ti ti-file-text me-2" ></i>Csv',
//             className: 'dropdown-item',
//             exportOptions: {
//               columns: [1, 2, 3, 4],
//               // prevent avatar to be display
//               format: {
//                 body: function (inner, coldex, rowdex) {
//                   if (inner.length <= 0) return inner;
//                   var el = $.parseHTML(inner);
//                   var result = '';
//                   $.each(el, function (index, item) {
//                     if (item.classList !== undefined && item.classList.contains('user-name')) {
//                       result = result + item.lastChild.firstChild.textContent;
//                     } else if (item.innerText === undefined) {
//                       result = result + item.textContent;
//                     } else result = result + item.innerText;
//                   });
//                   return result;
//                 }
//               }
//             }
//           },
//           {
//             extend: 'excel',
//             text: '<i class="ti ti-file-spreadsheet me-2"></i>Excel',
//             className: 'dropdown-item',
//             exportOptions: {
//               columns: [1, 2, 3, 4],
//               // prevent avatar to be display
//               format: {
//                 body: function (inner, coldex, rowdex) {
//                   if (inner.length <= 0) return inner;
//                   var el = $.parseHTML(inner);
//                   var result = '';
//                   $.each(el, function (index, item) {
//                     if (item.classList !== undefined && item.classList.contains('user-name')) {
//                       result = result + item.lastChild.firstChild.textContent;
//                     } else if (item.innerText === undefined) {
//                       result = result + item.textContent;
//                     } else result = result + item.innerText;
//                   });
//                   return result;
//                 }
//               }
//             }
//           },
//           {
//             extend: 'pdf',
//             text: '<i class="ti ti-file-code-2 me-2"></i>Pdf',
//             className: 'dropdown-item',
//             exportOptions: {
//               columns: [1, 2, 3, 4],
//               // prevent avatar to be display
//               format: {
//                 body: function (inner, coldex, rowdex) {
//                   if (inner.length <= 0) return inner;
//                   var el = $.parseHTML(inner);
//                   var result = '';
//                   $.each(el, function (index, item) {
//                     if (item.classList !== undefined && item.classList.contains('user-name')) {
//                       result = result + item.lastChild.firstChild.textContent;
//                     } else if (item.innerText === undefined) {
//                       result = result + item.textContent;
//                     } else result = result + item.innerText;
//                   });
//                   return result;
//                 }
//               }
//             }
//           },
//           {
//             extend: 'copy',
//             text: '<i class="ti ti-copy me-2" ></i>Copy',
//             className: 'dropdown-item',
//             exportOptions: {
//               columns: [1, 2, 3, 4],
//               // prevent avatar to be display
//               format: {
//                 body: function (inner, coldex, rowdex) {
//                   if (inner.length <= 0) return inner;
//                   var el = $.parseHTML(inner);
//                   var result = '';
//                   $.each(el, function (index, item) {
//                     if (item.classList !== undefined && item.classList.contains('user-name')) {
//                       result = result + item.lastChild.firstChild.textContent;
//                     } else if (item.innerText === undefined) {
//                       result = result + item.textContent;
//                     } else result = result + item.innerText;
//                   });
//                   return result;
//                 }
//               }
//             }
//           }
//         ]
//       },
//       {
//         text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">مرض جديد</span>',
//         className: 'add-new btn btn-primary waves-effect waves-light',
//         attr: {
//           'data-bs-toggle': 'offcanvas',
//           'data-bs-target': '#offcanvasAddUser'
//         }
//       }
//     ],
//     // For responsive popup
//     responsive: {
//       details: {
//         display: $.fn.dataTable.Responsive.display.modal({
//           header: function (row) {
//             var data = row.data();
//             return 'Details of ' + data['name'];
//           }
//         }),
//         type: 'column',
//         renderer: function (api, rowIdx, columns) {
//           var data = $.map(columns, function (col, i) {
//             return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
//               ? '<tr style="width: 100%; height: 100%;" data-dt-row="' +
//                   col.rowIndex +
//                   '" data-dt-column="' +
//                   col.columnIndex +
//                   '">' +
//                   '<td>' +
//                   col.title +
//                   ':' +
//                   '</td> ' +
//                   '<td>' +
//                   col.data +
//                   '</td>' +
//                   '</tr>'
//               : '';
//           }).join('');
//           return data ? $('<table class="table"/><tbody />').append(data) : false;
//         }
//       }
//     },
//     initComplete: function () {
//       // Adding backage filter once table initialized
//       this.api()
//       .columns(5) // Assuming status is in the 5th column (index 4)
//       .every(function () {
//         var column = this;
//         var select = $(
//           '<select class="form-select" id="status-filter">' +
//             '<option value="">اختر الحالة</option>' +
//           '</select>'
//         )
//         .appendTo('.diseases_status')
//         .on('change', function () {
//           var val = $.fn.dataTable.util.escapeRegex($(this).val());
//           column.search(val ? val : '', true, false).draw(); 
//         });
      
//         // Populate the dropdown with status options from statusObj
//         var statusOptions = [
//           "متاح للتشخيص",
//           "ليس متاحاً للتشخيص"
//         ];
      
//         for (const status of statusOptions) {
//           select.append(
//             '<option value="' +
//               status + 
//               '" class="text-capitalize">' +
//               status +
//               '</option>'
//           );
//         }
//       });
//     }
//   });

// })
// .catch((error)=>{console.error('Error fetching data:', error)})
// }


// $(function () {
// getDiseasesData();
// });