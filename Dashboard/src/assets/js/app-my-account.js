import {fetchAllData, submitRequest } from './api.js';
import { showAlert } from './general-function.js';
'use strict';
let userId;
function updateFormFields(data) {
  
  const avatarElement = document.getElementById('uploadedAvatar');
  // Check if the user has a profile picture, otherwise set a default image
  if (data.profile_picture) {
    avatarElement.src = data.profile_picture;
  } else {
    avatarElement.src = '/static/img/avatars/avatar-unknown.jpg';
}
  userId = data.id;
  document.getElementById('first-name').value = data.first_name || '';
  document.getElementById('last-name').value = data.last_name || '';
  document.getElementById('email').value = data.email || '';
  document.getElementById('phone-number').value = data.phone_number || '';
  document.getElementById('gender').value = data.gender || 'ذكر';
  document.getElementById('bs-datepicker-autoclose-birthdate').value = data.birth_date || '';
}




/**
 * Fetches patient profile data and initializes the profile display.
 */
async function fetchAndInitializeData() {
  const url_get_user_profile_data = `/users/api/profile/`;
  try {
    const data = await fetchAllData(url_get_user_profile_data);
    updateFormFields(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات الحساب:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeData);


/**
 * Handles the submission of the edit user form, updating the user data.
 */
document.getElementById('formAccountSettings').addEventListener('submit', async function (event) {
  event.preventDefault();
      const formData = new FormData();
      formData.append('first_name', document.getElementById('first-name').value);
      formData.append('last_name', document.getElementById('last-name').value);
      formData.append('phone_number', document.getElementById('phone-number').value);
      formData.append('gender', document.getElementById('gender').value);
      formData.append('birth_date', document.getElementById('bs-datepicker-autoclose-birthdate').value);
      
    // Check if a profile picture is uploaded, and add it to the form data
    const upload = document.getElementById('upload').files[0];
      if (upload) {
          formData.append('profile_picture', upload);
      }

      const method = 'PUT';
      const url = `/users/api/update/${userId}/`;
      try {
        const result = await submitRequest(url, method, formData );        
        if (result.success) {
          showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
          fetchAndInitializeData();
        }
        else {
          showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }
});

