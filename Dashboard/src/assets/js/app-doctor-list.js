import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';



/**
 * Page User List
 */

//دالة جلب البيانات عن طريقapi
async function fetchAndInitializeTable() {
  const url_get_doctors_data = '/doctors/api/getDoctors/';
  try {
    const data = await fetchAllData(url_get_doctors_data);
    console.log(data);
    fetchDataToDatatable(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات الأطباء:', error);
  }
}


'use strict';
var dt_doctor_table = $('.datatables-doctor'); //تعريف متغبر للجدول 

// دالة لأخذ البانات ووضعها داخل الجدول
function fetchDataToDatatable(data) {

  let all_doctors_count = 0;
  let active_doctors_count = 0;
  let non_active_doctors_count = 0;

  if ($.fn.DataTable.isDataTable(dt_doctor_table)) {
    dt_doctor_table.DataTable().clear().destroy();
  }

  var dt_doctor = dt_doctor_table.DataTable({
    data: data.doctors,
    columns: [
      { data: null },  // Empty column for responsive control
      { data: 'user.first_name' },
      { data: 'specialization' },
      { data: 'hospital' },
      { data: 'status_consults' },
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
          var name = `${full['user'].first_name} ${full['user'].last_name}`;
          var email = full['user'].email;
          var image = full['user'].profile_picture;
          var output;
          if (image) {
            output = `<img src="${image}" alt="Avatar" class="rounded-circle">`;
          } else {
            var initials = `${full['user'].first_name[0]}${full['user'].last_name[0]}`;
            var stateNum = Math.floor(Math.random() * 6);
            var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
            var state = states[stateNum];
            output = `<span class="avatar-initial rounded-circle bg-label-${state}">${initials}</span>`;
          }

          var doctorId = full['id'];
          var doctorProfileUrl = `/doctors/profile/${doctorId}/`;
          return `
            <div class="d-flex justify-content-start align-items-center user-name">
              <div class="avatar-wrapper">
                <div class="avatar me-3">
                  ${output}
                </div>
              </div>
              <div class="d-flex flex-column">
                <a href="${doctorProfileUrl}" class="text-body text-truncate">
                  <span class="fw-medium">${name}</span>
                </a>
                <small class="text-muted">${email}</small>
              </div>
            </div>`;
        }
      },
      {
        targets: 2,
        render: function (data, type, full, meta) {
          var $specialization = full['specialization'];

          // الأيقونة الخاصة بالتخصص
          var defaultIcon = '<span class="badge badge-center rounded-pill bg-label-info w-px-30 h-px-30 me-2"><i class="ti ti-stethoscope ti-sm"></i></span>';

          // بناء النص مع الأيقونة والتخصص
          return "<span class='text-truncate d-flex align-items-center'>" + defaultIcon + $specialization + '</span>';

        }
      },
      {
        targets: 3,
        render: function (data, type, full, meta) {
          var $address = full['address'];
          var $hospital = full['hospital'];
          if ($hospital) {
            return "<span class='text-truncate align-items-center'>" +
              '<span class="badge badge-center rounded-pill bg-label-primary w-px-30 h-px-30 me-2"><i class="ti ti-building-hospital ti-sm"></i></span>' +
              '<span class="fw-medium">' + $hospital + '</span>' +
              '<div class="fw-light px-5" style="font-size: 0.8rem;">' + $address + '</div>' +
              '</span>';
          } else {
            return "<span class='text-truncate d-flex align-items-center'>" +
              '<span class="badge badge-center rounded-pill bg-label-danger w-px-30 h-px-30 me-2"><i class="ti ti-x ti-sm"></i></span>' +
              '<span class="fw-medium">غير محدد</span>' +
              '</span>';
          }
        }
      },
      {
        targets: 4,
        render: function (data, type, full, meta) {
          var $consults =  full['total_consultations'] || 0;
          var $responded_consults = full['completed_consultations'] || 0;
          var $non_responded_consults = $consults - $responded_consults;

          return (
            '<span class="badge bg-label-secondary text-capitalized">' +
            $consults +
            '</span>' +
            ' <span class="badge bg-label-success text-capitalized">' +
            $responded_consults +
            '</span>' +
            ' <span class="badge bg-label-warning text-capitalized">' +
            $non_responded_consults +
            '</span>'
          );
        }
      },
      {
        targets: -1,
        title: 'Actions',
        data: null,
        searchable: false,
        orderable: false,
        render: function (data, type, full, meta) {
          var doctorId = full['id'];
          var doctorProfileUrl = `/doctors/profile/${doctorId}/`;
          return `
            <div class="d-flex align-items-center">
              <a href="${doctorProfileUrl}" class="text-body">
                <i class="ti ti-eye ti-sm me-2"></i>
              </a>
              <a href="javascript:;" class="text-body delete-record" data-id="${doctorId}">
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
          { extend: 'excel', text: 'Excel', className: 'dropdown-item' },
          { extend: 'pdf', text: '<i class="ti ti-file-description me-2"></i>Pdf', className: 'dropdown-item' },
          { extend: 'copy', text: '<i class="ti ti-copy me-2"></i>Copy', className: 'dropdown-item' }
        ]
      },
      {
        text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">اضافة طبيب جديد</span>',
        className: 'add-new btn btn-primary waves-effect waves-light',
        attr: {
          'data-bs-toggle': 'offcanvas',
          'data-bs-target': '#offcanvasAddDoctor'
        }
      }
    ],
  });

  $('#select-user-id').empty();

  //عرض اسماء المستخدمين غير الاطباء لفورم الاضافة
  $.each(data.users, function (index, user) {
    // تحقق من أن نوع المستخدم ليس طبيبًا وأن الاسم الأول أو الأخير ليس فارغًا
    if (user.user_type !== 'doctor' && (user.first_name.trim() !== '' || user.last_name.trim() !== '')) {
      // إضافة خيار جديد لقائمة الاختيار مع الاسم الكامل كاسم والقيمة هي المعرف
      $('#select-user-id').append(new Option(user.first_name + ' ' + user.last_name, user.id));

    }
  });


//حساب الاحصائيات حق الاطباء
  $.each(data.doctors, function (index, doctor) {
    all_doctors_count++;
    if (doctor.user.is_active) {
      active_doctors_count++;
    } else {
      non_active_doctors_count++;
    }
  });

  //حساب النسب المئوية
  let active_doctors_percentage = 0;
  let non_active_doctors_percentage = 0;

  if (all_doctors_count > 0) {
    active_doctors_percentage = (active_doctors_count / all_doctors_count) * 100;
    non_active_doctors_percentage = (non_active_doctors_count / all_doctors_count) * 100;
  }
  // تقريبهما لأقرب عدد صحيح
  active_doctors_percentage = Math.round(active_doctors_percentage);
  non_active_doctors_percentage = Math.round(non_active_doctors_percentage);

// تضمين القيم في العناصر
  $('#total-doctors').text(all_doctors_count);
  $('#active-doctors').text(active_doctors_count);
  $('#non-active-doctors').text(non_active_doctors_count);

  $('#active_doctors_percentage').text(active_doctors_percentage + "%");
  $('#non_active_doctors_percentage').text(non_active_doctors_percentage + "%");
}




// الدالة الرئيسية التي يتم استعداؤها عند فتح الصفحة
$(function () {

  fetchAndInitializeTable();


});

// document.getElementById('addNewDoctorForm').addEventListener('submit', function(event){
// alert('nothing');
// });

// // اضافة طبيب  
// اضافة طبيب  
document.getElementById('addNewDoctorForm').addEventListener('submit', async function (event) {
  // منع إرسال النموذج الافتراضي
  event.preventDefault();

  // الحصول على القيم من الحقول المدخلة
  const userId = document.getElementById('select-user-id').value;
  const specialization = document.getElementById('doctor-specialization').value;
  const hospital = document.getElementById('hospita-or-center').value;
  const address = document.getElementById('center-address').value;
  const activeOrNot = document.getElementById('active-or-not').checked;

  // التحقق من اختيار المستخدم
  if (!userId) {
    showAlert('error', 'فشل!', 'يرجى اختيار مستخدم لإضافته كطبيب.');
    return;
  }

  // إعداد البيانات للإرسال
  const formData = new FormData();
  formData.append('user', userId);
  formData.append('specialization', specialization);
  formData.append('hospital', hospital);
  formData.append('address', address);
  formData.append('active_or_not', activeOrNot);



  // إرسال الطلب باستخدام الدالة submitRequest
  const add_doctor_url = '/doctors/api/add_Doctors/';
  const method = 'POST'
  try {
    const result = await submitRequest(add_doctor_url, method, formData, {

    });

    if (result.success) {
      const offcanvasElement = document.getElementById('offcanvasAddDoctor');
      const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
      if (offcanvas) {
        offcanvas.hide();
      }
      showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');

      fetchAndInitializeTable();

      document.getElementById('addNewDoctorForm').reset();
    } else {
      showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
    }
  } catch (error) {
    console.error('Error adding doctor:', error);
    showAlert('error', 'فشل!', 'حدث خطأ أثناء إضافة الطبيب.');
  }
});


// حذف طبيب
$(document).on('click', '.delete-record', async function () {
  var doctorId = $(this).data('id'); // الحصول على id المريض  
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
    const method = 'DELETE';
    const url = `/doctors/api/delete/Doctors/${doctorId}/`;
    const deleteResult = await submitRequest(url, method);

    if (deleteResult.success) {
      showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
      fetchAndInitializeTable();
    } else {
      showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
    }
  }
});
















