import {fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

// Select city
// --------------------------------------------------------------------
const citySelect = document.getElementById('modalEditUserAddress');
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
  document.getElementById('user-address').innerText = data.user.user_address;
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
  document.getElementById('modalEditUserAddress').value = data.user.user_address;
  document.getElementById('modalEditUserAddress').textContent = data.user.user_address;
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
  const url_get_cities_data = `/api/users/cities/`;
  try {
    const data = await fetchAllData(url_get_patient_profile_data);
    const cities_data = await fetchAllData(url_get_cities_data);
    showPatientProfile(data);
    initializeSelectData(cities_data.data, citySelect);
  } catch (error) {
    console.error('خطأ في جلب بيانات المريض:', error);
  }
}

function initializeSelectData(data, element){
  element.innerHTML = ''; // Clear existing options to avoid duplication
  
  data.forEach(city => {
    console.log("citi: ",city.name);
      const option = document.createElement('option');
      option.value = city.name;
      option.textContent = city.name;
      element.appendChild(option);      
  });
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
      formData.append('user_address', document.getElementById('modalEditUserAddress').value);
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






