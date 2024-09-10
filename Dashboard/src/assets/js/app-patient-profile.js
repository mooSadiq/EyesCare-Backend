import {fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


/**
 * Displays the patient's profile information on the page.
 */
let userId;
function showPatientProfile(data) {
  userId = data.user.id;
  const avatarElement = document.getElementById('user-avatar');
  // Check if the user has a profile picture, otherwise set a default image
  if (data.user.profile_picture) {
      avatarElement.src = data.user.profile_picture;
  } else {
      avatarElement.src = '/static/img/avatars/avatar-unknown.jpg';
  }
  document.getElementById('userType').innerText = data.user.user_type;
  const userTypeElement = document.getElementById('userType');
    // Set the user type text based on the user_type value
  const userType = data.user.user_type;
  if (userType === 'patient') {
      userTypeElement.innerText = 'مريض';
  } else if (userType === 'doctor') {
      userTypeElement.innerText = 'طبيب';
  } else if (userType === 'admin') {
      userTypeElement.innerText = 'أدمن';
  } else if (userType === 'support') {
      userTypeElement.innerText = 'فريق الدعم';
  } else {
      userTypeElement.innerText = 'مستخدم عادي';
  }

  // Populate the profile information fields with user data
  document.getElementById('user-ful-name').innerText = `${data.user.first_name} ${data.user.last_name}`;
  document.getElementById('patient-number').innerText = `#${data.id}`;
  document.getElementById('user-email').innerText = data.user.email;
  document.getElementById('user-phone').innerText = data.user.phone_number;
  document.getElementById('user-gender').innerText = data.user.gender;
  document.getElementById('user-birthdate').innerText = data.user.birth_date;
  document.getElementById('user-status').innerText = data.user.is_active? 'نشط' : 'غير نشط';
  document.getElementById('user-status').className = data.user.is_active ? 'badge bg-label-success' : 'badge bg-label-danger';
  document.getElementById('user-verification').innerText = data.user.is_blue_verified ? 'موثق' : 'غير موثق';
  document.getElementById('user-verification').className = data.user.is_blue_verified ? 'badge bg-label-success' : 'badge bg-label-danger';
  const confirmActiveAlert = document.getElementById('confirm-active-alert');
  const isActive = data.user.is_active;
  // Set the activation button text and style based on user active status
  if (isActive) {
    confirmActiveAlert.textContent = 'الغاء تنشيط';
    confirmActiveAlert.classList.add('bg-label-danger');
  } else {
    confirmActiveAlert.textContent = 'تنشيط';
    confirmActiveAlert.classList.add('bg-label-success');
  }  

  // Update the edit form fields with user data
  document.getElementById('modalEditUserFirstName').value = data.user.first_name;
  document.getElementById('modalEditUserLastName').value = data.user.last_name;
  document.getElementById('modalEditUserEmail').value = data.user.email;
  document.getElementById('modalEditUserPhone').value = data.user.phone_number;
  document.getElementById('modalEditUsergender').value = data.user.gender;
  document.getElementById('bs-datepicker-autoclose-birthdate').value = data.user.birth_date;
  document.getElementById('modalEditUserRole').value = data.user.user_type;

  const verificationCheckbox = document.getElementById('switch-input-verified');
  verificationCheckbox.checked = data.user.is_blue_verified;
}

/**
 * Fetches patient profile data and initializes the profile display.
 */
async function fetchAndInitializeData() {
  const url_get_patient_profile_data = `/patients/api/get/patients/${getId}/`;
  try {
    const data = await fetchAllData(url_get_patient_profile_data);
    showPatientProfile(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات المريض:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeData);

/**
 * Handles the submission of the edit user form, updating the user data.
 */
document.getElementById('editUserForm').addEventListener('submit', async function (event) {
  event.preventDefault();
      const formData = new FormData();
      formData.append('first_name', document.getElementById('modalEditUserFirstName').value);
      formData.append('last_name', document.getElementById('modalEditUserLastName').value);
      formData.append('phone_number', document.getElementById('modalEditUserPhone').value);
      formData.append('gender', document.getElementById('modalEditUsergender').value);
      formData.append('birth_date', document.getElementById('bs-datepicker-autoclose-birthdate').value);
      formData.append('user_type', document.getElementById('modalEditUserRole').value);
      
    // Check if a profile picture is uploaded, and add it to the form data
    const upload = document.getElementById('modalEditUserFile').files[0];
      if (upload) {
          formData.append('profile_picture', upload);
      }
      // Set the blue verification status based on the checkbox
      const isBlueVerified = document.getElementById('switch-input-verified').checked ? '1' : '0';
      formData.append('is_blue_verified', isBlueVerified);
      const method = 'PUT';
      const url = `/users/api/update/${userId}/`;
      try {
        const result = await submitRequest(url, method, formData );        
        if (result.success) {
          const modalElement = document.getElementById('editUser');
          const modal = bootstrap.Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          }
          showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
          fetchAndInitializeData();
          this.reset();
        }
        else {
          showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }
});


/**
 * Handles the activation or deactivation of the user account.
 */
$(document).on('click', '#confirm-active-alert', async function () {
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
    const method = 'POST';
    const url = `/users/api/activation/${userId}/`;
    const activeResult = await submitRequest(url, method);
    if(activeResult.success) {
      fetchAndInitializeData();
      showAlert('success',  activeResult.data.is_active ? 'تم التنشيط!' : 'تم إلغاء التنشيط!', activeResult.message, 'btn btn-success');
    }
    else {
      showAlert('error', 'حدث خطأ!', activeResult.message, 'btn btn-danger');
    }
  }
});




$(function () {

  // Variable declaration for table
  var dt_diagnosis_table = $('.datatable-diagnosis'),
    dt_invoice_table = $('.datatable-consultations'),
    userView = "http://127.0.0.1:8000/patients/profile",
    diagnosesView = "http://127.0.0.1:8000/diagnosis/details";

  // Project datatable
  // --------------------------------------------------------------------
  if (dt_diagnosis_table.length) {
    var dt_diagnosis = dt_diagnosis_table.DataTable({
      ajax: assetsPath + 'json/patient-diagnosis-list.json', // JSON file to add data
      columns: [
        // columns according to JSON
        { data: '' },
        { data: 'id' },
        { data: 'result' },
        { data: 'date' },
        { data: '' }
      ],
      columnDefs: [
        {
          // For Responsive
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
          // 
          targets: 1,
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            var $image = full['diagnosis_image'];
            // For  image
            var $output = '<img src="' + assetsPath + 'img/elements/' + $image + '" alt="diagnosis Image" class="" style="width: 100%; height: 50px; border-radius: 10px;">';
            return $output; // Return only the image
          }
        },
        {
          // result 
          targets: 2,
          orderable: false,
          render: function (data, type, full, meta) {
            var $result = full['result'];
            return '<span class="fw-medium">' + $result + '</span>';
          }
        },
        {
          // date 
          targets: 3,
          render: function (data, type, full, meta) {
            var $date = full['date'];
            return '<span class="fw-medium">' + $date + '</span>';
          }
        },
        {
          // Actions
          targets: -1,
          title: 'المزيد',
          data: null,
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class=" align-items-center text-center">' +
              '<a href="' +
              diagnosesView +
              '" class="text-body"><i class="ti ti-eye ti-sm me-2"></i></a>' +
              '</div>'
            );
          }
        }
      ],
      order: [[1, 'asc']],
      dom:
        '<"d-flex justify-content-between align-items-center flex-column flex-sm-row mx-4 row"' +
        '<"col-sm-4 col-12 d-flex align-items-center justify-content-sm-start justify-content-center"l>' +
        '<"col-sm-8 col-12 d-flex align-items-center justify-content-sm-end justify-content-center"f>' +
        '>t' +
        '<"d-flex justify-content-between mx-4 row"' +
        '<"col-sm-12 col-md-6"i>' +
        '<"col-sm-12 col-md-6"p>' +
        '>',
      displayLength: 7,
      lengthMenu: [7, 10, 25, 50, 75, 100],
      language: {
        sLengthMenu: 'Show _MENU_',
        // search: '',
        searchPlaceholder: 'البحث'
      },
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'Details of ' + data['id'];
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
      }
    });
  }

  // Invoice datatable
  // --------------------------------------------------------------------
  if (dt_invoice_table.length) {
    var dt_invoice = dt_invoice_table.DataTable({
      ajax: assetsPath + 'json/consultations-list.json', // JSON file to add data
      columns: [
        // columns according to JSON
        { data: '' },
        { data: 'full_name' },
        { data: 'date' },
        { data: 'status' },
        { data: '' }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          responsivePriority: 2,
          targets: 0,
          render: function (data, type, full, meta) {
            return '';
          }
        },
        {
          // doctor full name and email
          targets: 1,
          responsivePriority: 4,
          render: function (data, type, full, meta) {
            var $name = full['full_name'],
              $email = full['email'],
              $image = full['avatar'];
            if ($image) {
              // For Avatar image
              var $output =
                '<img src="' + assetsPath + 'img/avatars/' + $image + '" alt="Avatar" class="rounded-circle">';
            } else {
              // For Avatar badge
              var stateNum = Math.floor(Math.random() * 6);
              var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
              var $state = states[stateNum],
                $name = full['full_name'],
                $initials = $name.split(' ').map(word => word[0]).join(' ');
              $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $initials + '</span>';
            }
            // Creates full output for row
            var $row_output =
              '<div class="d-flex justify-content-start align-items-center user-name">' +
              '<div class="avatar-wrapper">' +
              '<div class="avatar me-3">' +
              $output +
              '</div>' +
              '</div>' +
              '<div class="d-flex flex-column">' +
              '<a href="' +
              userView +
              '" class="text-body text-truncate"><span class="fw-medium">' +
              $name +
              '</span></a>' +
              '<small class="text-muted">' +
              $email +
              '</small>' +
              '</div>' +
              '</div>';
            return $row_output;
          }
        },
        {
          // date 
          targets: 2,
          render: function (data, type, full, meta) {
            var $date = full['date'];
            return '<span class="fw-medium">' + $date + '</span>';
          }
        },
        {
          // status
          targets: 3,
          render: function (data, type, full, meta) {
            var $status = full['status'];
          
            if ($status === "0") {
              return (
                '<span class="badge bg-label-warning">' +
                "قيد الانتظار" +
                '</span>'
              );
            } else {
              return (
                '<span class="badge bg-label-success">' +
                "انتهت" +
                '</span>'
              );
            }
          }
        },
        {
          // Actions
          targets: -1,
          title: 'المزيد',
          data: null,
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class=" align-items-center text-center">' +
              '<a href="' +
              userView +
              '" class="text-body"><i class="ti ti-eye ti-sm me-2"></i></a>' +
              '</div>'
            );
          }
        }
      ],
      order: [[1, 'asc']],
      dom:
        '<"row mx-4"' +
        '<"col-sm-6 col-12 d-flex align-items-center justify-content-center justify-content-sm-start mb-3 mb-md-0"l>' +
        '<"col-sm-6 col-12 d-flex align-items-center justify-content-center justify-content-sm-end"B>' +
        '>t' +
        '<"row mx-4"' +
        '<"col-md-12 col-lg-6 text-center text-lg-start pb-md-2 pb-lg-0"i>' +
        '<"col-md-12 col-lg-6 d-flex justify-content-center justify-content-lg-end"p>' +
        '>',
      language: {
        sLengthMenu: 'Show _MENU_',
        search: '',
        searchPlaceholder: 'Search Invoice'
      },
      // Buttons with Dropdown
      buttons: [
        {
          extend: 'collection',
          className: 'btn btn-label-secondary dropdown-toggle float-sm-end mb-3 mb-sm-0 waves-effect waves-light',
          text: '<i class="ti ti-screen-share ti-xs me-2"></i>Export',
          buttons: [
            {
              extend: 'print',
              text: '<i class="ti ti-printer me-2" ></i>Print',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'csv',
              text: '<i class="ti ti-file-text me-2" ></i>Csv',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'excel',
              text: '<i class="ti ti-file-spreadsheet me-2"></i>Excel',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'pdf',
              text: '<i class="ti ti-file-description me-2"></i>Pdf',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'copy',
              text: '<i class="ti ti-copy me-2" ></i>Copy',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            }
          ]
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
      }
    });
  }
  // On each datatable draw, initialize tooltip
  dt_invoice_table.on('draw.dt', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl, {
        boundary: document.body
      });
    });
  });

  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
  }, 300);
});



