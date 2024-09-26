const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function getToken(key) {
  return localStorage.getItem(key);
}


function isTokenExpired(token) {
  if (!token) return true;

  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid token format');
  }
  const payload = JSON.parse(atob(parts[1]));
  const now = Math.floor(Date.now() / 1000); 
  return payload.exp < now;
}



 async function refreshToken() {
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
      localStorage.setItem('access_token', newAccessToken);
      return newAccessToken;
  } else {
      await fetch('/auth/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${refreshToken}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({}),
        });
        window.location.href = '/auth/login/'; 
        throw new Error('Failed to refresh token and logged out');
  }
}

async function fetchWithAuth(url, options = {}) {
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
async function submitRequest(url, method, options = {}) {
    try {
        const response = await fetchWithAuth(url, {
            method: method,
            headers: {
                'X-CSRFToken': csrfToken,
                ...options.headers 
            },
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


async function fetchAllData(url) {
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

function toJson(data) {
    let jsonString = data;
    jsonString = jsonString.replace(/'/g, '"');
    try {
        const jsObject = JSON.parse(jsonString);
        return jsObject;
    } catch (parseError) {
        console.error("Error parsing JSON:", parseError);
        return "Undefined"
    }
}


function add_item(notification,listofnotifications){
    let notification_id=notification.id;
    let user_id=parseInt(notification.action_object_object_id);
    let type=toJson(notification.data);
    type=type.category;
    const list_item = `
<li class="list-group-item list-group-item-action dropdown-notifications-item">
        ${type == "Rateing" ? `
        <div class="d-flex">
        <div class="flex-shrink-0 me-3">
        <div class="avatar">
            <span class="avatar-initial rounded-circle bg-label-danger">Ra</span>
        </div>
        </div>
            <div class="flex-grow-1">
        <a href="evaluations/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == "Consultation" ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-secondary">Con</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="#" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == "DiagnosisReport" ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-primary">Dia</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="diagnosis/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == "Doctor" ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-info">Doc</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="doctors/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == "Patient" ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-danger">Pa</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="patients/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == "Post" ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-warning">Po</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="posts/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : type == 'User' ? `
    <div class="d-flex">
    <div class="flex-shrink-0 me-3">
    <div class="avatar">
        <span class="avatar-initial rounded-circle bg-label-success">User</span>
    </div>
    </div>
        <div class="flex-grow-1">
        <a href="users/" onclick="read(${notification_id})">
            <h6 class="mb-1">${notification.verb}</h6>
            <p class="mb-0">${notification.description}</p>
        </a>`
    : ''
    }
        <small class="text-muted">${notification.timestamp}</small>
        </div>
        <div class="flex-shrink-0 dropdown-notifications-actions">
            ${notification.unread == 1 ? `
            <a href="javascript:void(0)" class="dropdown-notifications-read">
                <span class="badge badge-dot"></span>
            </a>` : ''}
            <a href="javascript:void(0)" class="dropdown-notifications-archive" onclick="delete_notifictions(${notification_id})">
                <span class="ti ti-x"></span>
            </a>
        </div>
    </div>
</li>`;
    listofnotifications.innerHTML += list_item;
}
function showPatientProfile(data) {
    document.getElementById('noti-count').innerText = data.count;
    notifications=data.data
    listofnotifications=document.getElementById('notification-list')
    for(let i=0;i<notifications.length;i++){
        add_item(notifications[i],listofnotifications);
    }
}

async function fetchAndInitializelist() {
    const url_get_deseases_data = '/notifications/get/all/';
    try {
        const data = await fetchAllData(url_get_deseases_data);
        showPatientProfile(data);
        console.log(data.data);
    } catch (error) {
        console.error('خطأ في جلب بيانات :', error);
    }
    
}
document.addEventListener('DOMContentLoaded', fetchAndInitializelist);

async function read(notification_id){
    const method = 'POST';
            const url = `/notifications/read/${notification_id}/`;
            try {
            const result = await submitRequest(url, method);
            if (result.success) {
                fetchAndInitializelist()
                this.reset();
            }
            else {
                showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
            }
            } catch (error) {
            console.error('Error updating data:', error);
            }
}

async function read_all(){
    const method = 'POST';
            const url = `/notifications/read/all/`;
            try {
            const result = await submitRequest(url, method);
            if (result.success) {
                window.location.href = '';
                fetchAndInitializelist() 
                this.reset();
            }
            else {
                showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
            }
            } catch (error) {
            console.error('Error updating data:', error);
            }
}

async function delete_notifictions(notification_id){
    const method = 'DELETE';
    const url = `/notifications/delete/${notification_id}/`;
    const deleteResult = await submitRequest(url, method);
    if (deleteResult.success) {
        window.location.href = '';
        fetchAndInitializelist();
    } else {
        showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
    }
}

