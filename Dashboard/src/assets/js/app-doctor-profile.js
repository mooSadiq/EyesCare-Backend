/**
 * App Doctor Profile -  (jquery)
 */
import {fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


const confirmActiveAlert = document.querySelector('#confirm-active-alert');

// دالة لجلب بيانات المريض من api
async function fetchdoctorData(getId) {

    const url_get_doctor_profile_data = `/doctors/api/getDoctors/${getId}/`;
    try {
      const data = await fetchAllData(url_get_doctor_profile_data);
      updatedoctorProfile(data);
    } catch (error) {
      console.error('خطأ في جلب بيانات الطبيب:', error);
    }
}

let userId;
let doctor_Id;

// دالة لتحديث واجهة بي ببيانات المريض التي تم ارجاعها في الدالة السابقة 
function updatedoctorProfile(data) {
  
  userId = data.user.id;
  
  doctor_Id = data.id;
  const avatarElement = document.getElementById('doctor-avatar');
  // التحقق من وجود صورة للمستخدم أو تعيين الصورة الافتراضيةة
  if (data.user.profile_picture) {
      avatarElement.src = data.user.profile_picture;
  } else {
      avatarElement.src = '/static/img/avatars/avatar-unknown.jpg';
  }
  document.getElementById('userType').innerText = data.user.user_type;
  const userTypeElement = document.getElementById('userType');
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

  document.getElementById('doctor-name').innerText = `${data.user.first_name} ${data.user.last_name}`;
  document.getElementById('doctor-number').innerText = `#${data.id}`;
  document.getElementById('doctor-email').innerText = data.user.email;
  document.getElementById('doctor-phone').innerText = data.user.phone_number;
  document.getElementById('doctor-gender').innerText = data.user.gender;
  document.getElementById('doctor-birthdate').innerText = data.user.birth_date;
  document.getElementById('doctor-status').innerText = data.user.is_active ? 'نشط' : 'غير نشط';
  document.getElementById('doctor-status').className = data.user.is_active ? 'badge bg-label-success' : 'badge bg-label-danger';
  document.getElementById('doctor-verification').innerText = data.user.is_blue_verified ? 'موثق' : 'غير موثق';
  document.getElementById('doctor-verification').className = data.user.is_blue_verified ? 'badge bg-label-success' : 'badge bg-label-danger';
 
  document.getElementById('doctor-specialization').innerText = data.specialization;
  document.getElementById('doctor-hospital').innerText = data.hospital;
  document.getElementById('doctor-address').innerText = data.address;

  const isActive = data.user.is_active;
  // تحديث نص الزر بناءً على حالة المستخدم
  if (isActive) {
    confirmActiveAlert.textContent = 'الغاء تنشيط';
    confirmActiveAlert.classList.add('bg-label-danger');
  } else {
    confirmActiveAlert.textContent = 'تنشيط';
    confirmActiveAlert.classList.add('bg-label-success');
  }  

  // تحديث البيانات في فورم التعديل
  document.getElementById('modalEditUserFirstName').value = data.user.first_name;
  document.getElementById('modalEditUserLastName').value = data.user.last_name;
  document.getElementById('modalEditUserEmail').value = data.user.email;
  document.getElementById('modalEditUserPhone').value = data.user.phone_number;
  document.getElementById('modalEditUsergender').value = data.user.gender;
  document.getElementById('bs-datepicker-autoclose-birthdate').value = data.user.birth_date;
  document.getElementById('modalEditUserRole').value = data.user.user_type;

  document.getElementById('modalEditUserSpecialization').value = data.specialization;
  document.getElementById('modalEditUserHospital').value = data.hospital;
  document.getElementById('modalEditUserAddress').value = data.address;

  const verificationCheckbox = document.getElementById('switch-input-verified');
  verificationCheckbox.checked = data.user.is_blue_verified;
}

// دالة لارسال البيانات المعدلة وتحديثها  
async function updateUserData(event) {
  event.preventDefault();
  try {
      const formData = new FormData();
      const formData_2 = new FormData();
      formData.append('first_name', document.getElementById('modalEditUserFirstName').value);
      formData.append('last_name', document.getElementById('modalEditUserLastName').value);
      formData.append('phone_number', document.getElementById('modalEditUserPhone').value);

      formData_2.append('specialization', document.getElementById('modalEditUserSpecialization').value);
      formData_2.append('hospital', document.getElementById('modalEditUserHospital').value);
      formData_2.append('address', document.getElementById('modalEditUserAddress').value);

      formData.append('gender', document.getElementById('modalEditUsergender').value);
      formData.append('birth_date', document.getElementById('bs-datepicker-autoclose-birthdate').value);
      formData.append('user_type', document.getElementById('modalEditUserRole').value);

      // التحقق هل تم رقع صورة ام لا 
      const upload = document.getElementById('modalEditUserFile').files[0];
      if (upload) {
          formData.append('profile_picture', upload);
      }
      //   زر التوثيق يالشارة الزرقاء
      const isBlueVerified = document.getElementById('switch-input-verified').checked ? '1' : '0';
      formData.append('is_blue_verified', isBlueVerified);

      const method = 'PUT';
      const url = `/users/api/update/${userId}/`;
      try {
        const result = await submitRequest(url, method, formData );        
        if (result.success) {
          const modalElement = document.getElementById('editUser');
          const modal = bootstrap.Modal.getInstance(modalElement);
        //   if (modal) {
        //     modal.hide();
        //   }
          showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
          fetchdoctorData(doctor_Id);
          this.reset();
        }
        else {
          showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }


    //   حفظ بيانات الطبيب في جدول الأطباء بعد التعديل
      const method_2 = 'PUT';
      const url_2 = `/doctors/api/profile/update/${doctor_Id}/`;
      try {
        const result = await submitRequest(url_2, method_2, formData_2 );        
        if (result.success) {
          const modalElement = document.getElementById('editUser');
          const modal = bootstrap.Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          }
          showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
          fetchdoctorData(doctor_Id);
          this.reset();
        }
        else {
          showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }

    
  } catch (error) {
      console.error('هناك خطأعند تحيث البيانات:', error);
  }
}

// الدالة الرئيسية التي يتم استعداؤها عند فتح الصفحة
$(function () {
   
  fetchdoctorData(getId);
  document.getElementById('editUserForm').addEventListener('submit', updateUserData);


  // Variable declaration for table
  var dt_diagnosis_table = $('.datatable-diagnosis'),
    dt_invoice_table = $('.datatable-consultations'),
    userView = "http://127.0.0.1:8000/patients/profile",
    diagnosesView = "http://127.0.0.1:8000/diagnosis/details";

  // Project datatable
 

  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
  }, 300);
});


// Alert With Functional Confirm Button لتنشيط أو إلغاء تنشيط المستخدم
$(document).on('click', '#confirm-active-alert', async function () {
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
    const method = 'POST';
    const url = `/users/api/activation/${userId}/`;
    const activeResult = await submitRequest(url, method);
    if(activeResult.success) {
      fetchdoctorData(getId);
      showAlert('success',  activeResult.data.is_active ? 'تم التنشيط!' : 'تم إلغاء التنشيط!', activeResult.message, 'btn btn-success');
    }
    else {
      showAlert('error', 'حدث خطأ!', activeResult.message, 'btn btn-danger');
    }
  }
});
