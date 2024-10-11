
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

export function getToken(key) {
  return localStorage.getItem(key);
}


export function isTokenExpired(token) {
  if (!token) 
    window.location.href = '/auth/login/';
  

  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid token format');
  }
  const payload = JSON.parse(atob(parts[1]));
  const now = Math.floor(Date.now() / 1000); 
  return payload.exp < now;
}

export async function refreshToken() {
  const refreshToken = getToken('refresh_token');
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
      const refresh_token = getToken('refresh_token');
      await fetch('/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({refresh_token}),
      });
      window.location.href = '/auth/login/'; 
      throw new Error('Failed to refresh token and logged out');
  }
}
