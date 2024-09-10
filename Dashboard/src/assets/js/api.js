import { getToken, isTokenExpired, refreshToken } from './auth.js';
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


export async function fetchWithAuth(url, options = {}) {
  let accessToken = getToken('access_token');

  if (isTokenExpired(accessToken)) {
      try {
          accessToken = await refreshToken();
      } catch (error) {
          console.error('Failed to refresh token:', error);
          return null; 
      }
  }

  const headers = {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`,
  };
  const response = await fetch(url, {
      ...options,
      headers,
  });

  if (response.status === 401) {
      try {
          accessToken = await refreshToken();
          return fetch(url, {
              ...options,
              headers: {
                  ...options.headers,
                  'Authorization': `Bearer ${accessToken}`,
              },
          });
      } catch (error) {
          console.error('Failed to refresh token:', error);
          return null; 
      }
  }
  return response;
}



export async function fetchAllData(url) {
  try {
      const response = await fetchWithAuth(url, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      });

      if (!response.ok) {
          throw new Error('Response was not ok');
      }
      const data = await response.json();
      return data;
  } catch (error) {
      console.error('هناك خطأ في جلب البيانات:', error);
      return [];
  }
}


export async function submitRequest(url, method, formData, options = {}) {
  try {
      const response = await fetchWithAuth(url, {
          method: method,
          headers: {
              'X-CSRFToken': csrfToken,
              ...options.headers 
          },
          body: formData
      });

      if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message);
      }

      const data = await response.json();
      console.log(data.message);
      return {
          success: true,
          message: data.message,
          data:data,
      };
  } catch (error) {
      console.error('Error:', error);
      return {
          success: false,
          message: error.message
      };
  }
}
