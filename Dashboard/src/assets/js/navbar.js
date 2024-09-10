import {fetchAllData, submitRequest } from './api.js';
'use strict';
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
async function updateNavbar(data) {
  const accessToken = localStorage.getItem('access_token');

  document.getElementById('user-name').innerText = `${data.first_name} ${data.last_name}`;
  document.getElementById('user-role').innerText = data.user_type
  const avatarUrl = data.profile_picture;
  const image = new Image();
  image.onload = function() {
    document.getElementById('user-avatar1').src = avatarUrl;
    document.getElementById('user-avatar2').src = avatarUrl;
  };
  image.onerror = function() {
    document.getElementById('user-avatar1').src = '{% static "img/avatars/1.png" %}';
    document.getElementById('user-avatar2').src = '{% static "img/avatars/1.png" %}';
  };
  image.src = avatarUrl;

} 

/**
 * Fetches patient profile data and initializes the profile display.
 */
async function fetchAndInitializeData() {
  const url_get_user_profile_data = `/users/api/profile/`;
  try {
    const data = await fetchAllData(url_get_user_profile_data);
    updateNavbar(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات المستخدم:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchAndInitializeData);

export async function logoutRequest(url, method) {
  try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
          throw new Error('No refresh token provided.');
      }

      const response = await fetch(url, {
          method: method,
          headers: {
              'Authorization': `Bearer ${refreshToken}`,  // تأكد من استخدام Bearer مع التوكن
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json'
          },
      });

      if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Logout failed.');
      }

      const data = await response.json();
      console.log(data.message);
      
      // حذف التوكنات من الـ Local Storage بعد نجاح عملية تسجيل الخروج
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      return {
          success: true,
          message: data.message,
      };
  } catch (error) {
      console.error('Error during logout:', error);
      return {
          success: false,
          message: error.message
      };
  }
}

document.getElementById('form-logout').addEventListener('submit', async function (event) {
  event.preventDefault();
  const url = `/auth/logout/`;
  try {
    const result = await logoutRequest(url, 'POST');
    if (result.success) {
      console.log('Logout successful.');
      window.location.href = '/login/';
    } else {
      console.log('Logout failed.');
    }
  } catch (error) {
    console.error('Error during logout:', error);
  }
});



function logoutUser() {
  const refreshToken = localStorage.getItem('refresh_token');
  fetch('/auth/logout/', {
      method: 'POST',
      headers: {
          'Authorization': `Bearer ${refreshToken}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken 
      },
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      // حذف التوكنات من الـ Local Storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      // إعادة توجيه المستخدم إلى صفحة تسجيل الدخول بعد تسجيل الخروج
      window.location.href = '/auth/login/';
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}