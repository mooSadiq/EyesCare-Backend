import { getToken, isTokenExpired, handleLogout, refreshToken } from './auth.js';
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// export async function fetchWithAuth(url, options = {}) {
//   let accessToken = getToken('access_token');

//   if (!accessToken || isTokenExpired(accessToken)) {
//     try {
//       accessToken = await refreshToken();
//       if (!accessToken) {
//         await handleLogout();
//         return null; // لا يوجد توكن، إرجاع null
//       }
//     } catch (error) {
      
//       console.error('Failed to refresh token:', error);
//       await handleLogout();
//       return null; 
//     }
//   }

//   const headers = {
//     ...options.headers,
//     'Authorization': `Bearer ${accessToken}`,
//   };

//   const response = await fetch(url, {
//     ...options,
//     headers,
//   });

//   if (response.status === 401) {
//     try {
//       accessToken = await refreshToken();
//       if (!accessToken) {
//         await handleLogout();
//         return null; // لا يوجد توكن، إرجاع null
//       }
//       return fetch(url, {
//         ...options,
//         headers: {
//           ...options.headers,
//           'Authorization': `Bearer ${accessToken}`,
//         },
//       });
//     } catch (error) {
//       console.error('Failed to refresh token:', error);
//       await handleLogout();
//       return null; 
//     }
//   }
//   return response;
// }

export async function fetchWithAuth(url, options = {}) {
  let accessToken = getToken('access_token');

  // الخطوة 1: التحقق من وجود الـ access_token وصلاحيته
  if (!accessToken || isTokenExpired(accessToken)) {
    const refreshToken = getToken('refresh_token');

    // الخطوة 2: التحقق من وجود الـ refresh_token
    if (!refreshToken) {
      await handleLogout(); // تسجيل الخروج إذا لم يكن هناك refresh_token
      return null;
    }

    // الخطوة 3: التحقق من صلاحية الـ refresh_token
    if (isTokenExpired(refreshToken)) {
      await handleLogout(); // تسجيل الخروج إذا كان الـ refresh_token منتهي
      return null;
    }

    // الخطوة 4: محاولة تجديد الـ access_token باستخدام الـ refresh_token
    try {
      accessToken = await refreshToken();
      if (!accessToken) { // في حال فشل التجديد
        await handleLogout();
        return null;
      }
    } catch (error) {
      console.error('Failed to refresh token:', error);
      await handleLogout(); // تسجيل الخروج في حال فشل عملية التجديد
      return null;
    }
  }

  // الخطوة 5: إعداد الطلب مع الـ access_token المجدد أو الحالي
  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${accessToken}`,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // إذا كانت الاستجابة 401 (Unauthorized)، حاول تجديد التوكن مرة أخرى
  if (response.status === 401) {
    try {
      accessToken = await refreshToken();
      if (!accessToken) { // إذا فشل التجديد مرة أخرى
        await handleLogout();
        return null;
      }

      // إعادة محاولة الطلب مع الـ access_token المجدد
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${accessToken}`,
        },
      });
    } catch (error) {
      console.error('Failed to refresh token after 401:', error);
      await handleLogout(); // تسجيل الخروج في حال فشل التجديد بعد 401
      return null;
    }
  }

  return response; // إعادة الاستجابة النهائية
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
