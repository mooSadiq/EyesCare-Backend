'use strict';
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener('DOMContentLoaded', function () {
  const firstName = localStorage.getItem('user_first_name');
  const lastName = localStorage.getItem('user_last_name');
  const profileImage = localStorage.getItem('user_profile_picture');
  const email = localStorage.getItem('user_email');
  const user_type = localStorage.getItem('user_type'); 

  if (profileImage) {
    document.getElementById('user-avatar1').src = profileImage;
    document.getElementById('user-avatar2').src = profileImage;
  }

  if (firstName && lastName) {
    document.getElementById('user-name').textContent = `${firstName} ${lastName}`;
  }
  let userTypeInArabic = '';
  if (user_type === 'doctor') {
    userTypeInArabic = 'طبيب';
  } else if (user_type === 'admin') {
    userTypeInArabic = 'مدير';
  } else if (user_type === 'patient') {
    userTypeInArabic = 'مريض';
  } else if (user_type === 'user') {
    userTypeInArabic = 'مستخدم';
  } else {
    userTypeInArabic = 'غير معروف'; 
  }

  document.getElementById('user-role').textContent = userTypeInArabic;
});




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
      localStorage.removeItem('user_first_name');
      localStorage.removeItem('user_last_name');
      localStorage.removeItem('user_profile_picture');
      localStorage.removeItem('user_email');
      localStorage.removeItem('user_type');
      window.location.href = '/auth/login/';
    } else {
        console.log('Logout failed.');
    }
  }) 
  .catch(error => {
      console.error('Error:', error);
  });
});