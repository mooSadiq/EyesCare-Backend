/**
 * Dashboard eCommerce
 */
'use strict';
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
        'X-CSRFToken': csrfToken,
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
        ...options.headers,
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
      data: data,
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      success: false,
      message: error.message,
    };
  }
}

async function fetchAllData(url) {
  try {
    const response = await fetchWithAuth(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Response was not ok');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
}

async function fetchAndInitializeList() {
  const urlGetDiseasesData = '/statics/';
  try {
    const data = await fetchAllData(urlGetDiseasesData);
    let adsString = JSON.stringify(data.Ads_static); // This gives you a string
    let adsArray = JSON.parse(adsString); 
    do_data(adsArray)// Convert it back to an array or object
  } catch (error) {
    console.error('Error fetching disease data:', error);
  }
}

document.addEventListener('DOMContentLoaded', fetchAndInitializeList);

function do_data(data){
    let cardColor, labelColor, headingColor, borderColor, legendColor;

    cardColor = config.colors.cardColor;
    labelColor = config.colors.textMuted;
    legendColor = config.colors.bodyColor;
    headingColor = config.colors.headingColor;
    borderColor = config.colors.borderColor;
  
    // Donut Chart Colors
    const chartColors = {
      donut: {
        series1: '#22A95E',
        series2: '#24B364',
        series3: config.colors.success,
        series4: '#53D28C',
        series5: '#7EDDA9',
        series6: '#A9E9C5',
      },
    };
    const reportBarChartEl = document.querySelector('#reportBarChart'),
    reportBarChartConfig = {
      chart: {
        height: 230,
        type: 'bar',
        toolbar: {
          show: false,
        },
      },
      plotOptions: {
        bar: {
          barHeight: '60%',
          columnWidth: '60%',
          startingShape: 'rounded',
          endingShape: 'rounded',
          borderRadius: 4,
          distributed: true,
        },
      },
      grid: {
        show: false,
        padding: {
          top: -20,
          bottom: 0,
          left: -10,
          right: -10,
        },
      },
      colors: [
        config.colors_label.primary,
        config.colors_label.warning,
      ],
      dataLabels: {
        enabled: false,
      },
      series: [
        {
          data: data,
        },
      ],
      legend: {
        show: false,
      },
      xaxis: {
        categories: ['عدد المشاهدات', 'عدد النقرات'],
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
        labels: {
          style: {
            colors: labelColor,
            fontSize: '13px',
          },
        },
      },
      yaxis: {
        labels: {
          show: false,
        },
      },
      responsive: [
        {
          breakpoint: 1025,
          options: {
            chart: {
              height: 190,
            },
          },
        },
        {
          breakpoint: 769,
          options: {
            chart: {
              height: 250,
            },
          },
        },
      ],
    };

  if (typeof reportBarChartEl !== undefined && reportBarChartEl !== null) {
    const barChart = new ApexCharts(reportBarChartEl, reportBarChartConfig);
    barChart.render();
  }
}


