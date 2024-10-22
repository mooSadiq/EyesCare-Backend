
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

export function getToken(key) {
  return localStorage.getItem(key);
}

export function isTokenAvailable(key) {
  const token = localStorage.getItem(key);
  return token !== null; // دالة تتحقق من وجود التوكن بحيث تعيد ترو اذا كان التوكن موجود او فلس اذا كان غير موجود
}
export function isTokenExpired(token) {
  if (!token) {
    return true;
  }
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid token format');
  }
  const payload = JSON.parse(atob(parts[1]));
  const now = Math.floor(Date.now() / 1000); 
  return payload.exp < now;
}


export async function refreshToken() {
  try {
    const refreshToken = getToken('refresh_token');    
    if (isTokenExpired(refreshToken)) {
      await handleLogout(); 
      return; 
    }

    const response = await fetch('/auth/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      const newAccessToken = data.access;
      const newRefreshToken = data.refresh;

      localStorage.setItem('access_token', newAccessToken);
      localStorage.setItem('refresh_token', newRefreshToken);

      return newAccessToken; 
    } else {
      await handleLogout(); 
      return;
    }
  } catch (error) {
    console.error('Error refreshing token:', error.message);
    await handleLogout(); 
  }
}
// export async function refreshToken() {
//   const refreshToken = getToken('refresh_token');
//   if (!refreshToken || isTokenExpired(refreshToken)) {
//     handleLogout();  // 
//     return;
//   }
//   const response = await fetch('/auth/token/refresh/', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ refresh: refreshToken }),
//   });
  
//   if (response.ok) {
//       const data = await response.json();
//       const newAccessToken = data.access;
//       const newRefreshToken = data.refresh;
//       localStorage.setItem('access_token', newAccessToken);
//       localStorage.setItem('refresh_token', newRefreshToken);

//       return newAccessToken;
//   } else {
//     handleLogout(); 
//     throw new Error('Failed to refresh token and logged out');
//   }
// }

export async function handleLogout() {
  const refresh_token = getToken('refresh_token');


    await fetch('/auth/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ refresh: refresh_token }),
    });

  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/auth/login/'; // توجيه المستخدم إلى صفحة تسجيل الدخول
}

