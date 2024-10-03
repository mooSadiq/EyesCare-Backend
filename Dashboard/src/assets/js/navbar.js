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




document.getElementById('logout-btn').addEventListener('click', function() {
  const refreshToken = localStorage.getItem('refresh_token');

  if (!refreshToken) {
      alert("No refresh token found. Please login.");
      return;
  }
  fetch('/auth/logout/', { 
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`  
      },
      body: JSON.stringify({
          'refresh_token': refreshToken
      })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === true) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth/login/';
    } else {
        console.log('Logout failed.');
    }
  }) 
  .catch(error => {
      console.error('Error:', error);
  });
});