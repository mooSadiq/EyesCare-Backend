/**
 * Charts ChartsJS
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
    let adsString = JSON.stringify(data);
    let adsArray = JSON.parse(adsString);
    draw(adsArray)// Convert it back to an array or object
  } catch (error) {
    console.error('Error fetching disease data:', error);
  }
}

document.addEventListener('DOMContentLoaded', fetchAndInitializeList);
function draw(data) {
    // Color Variables
    const purpleColor = '#836AF9',
    yellowColor = '#ffe800',
    cyanColor = '#28dac6',
    orangeColor = '#FF8132';

  let cardColor, headingColor, labelColor, borderColor, legendColor;

    cardColor = config.colors.cardColor;
    headingColor = config.colors.headingColor;
    labelColor = config.colors.textMuted;
    legendColor = config.colors.bodyColor;
    borderColor = config.colors.borderColor;


  // Set height according to their data-height
  // --------------------------------------------------------------------
  const chartList = document.querySelectorAll('.chartjs');
  chartList.forEach(function (chartListItem) {
    chartListItem.height = chartListItem.dataset.height;
  });

  // Bar Chart
  // Bar Chart
  // --------------------------------------------------------------------
  const barChart = document.getElementById('barChart');
  if (barChart) {
    const barChartVar = new Chart(barChart, {
      type: 'bar',
      data: {
        labels: [
          'قيد الأنتظار',
          'متاح',
          'منهي',
          'محظور',
        ],
        datasets: [
          {
            data: data.Ads_status,
            backgroundColor: cyanColor,
            borderColor: 'transparent',
            maxBarThickness: 15,
            borderRadius: {
              topRight: 15,
              topLeft: 15
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 500
        },
        plugins: {
          tooltip: {
            rtl: isRtl,
            backgroundColor: cardColor,
            titleColor: headingColor,
            bodyColor: legendColor,
            borderWidth: 1,
            borderColor: borderColor
          },
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            grid: {
              color: borderColor,
              drawBorder: false,
              borderColor: borderColor
            },
            ticks: {
              color: labelColor
            }
          },
          y: {
            min: 0,
            max: 400,
            grid: {
              color: borderColor,
              drawBorder: false,
              borderColor: borderColor
            },
            ticks: {
              stepSize: 100,
              color: labelColor
            }
          }
        }
      }
    });
  }



  // Polar Chart
  // --------------------------------------------------------------------

  const polarChart = document.getElementById('polarChart');
  if (polarChart) {
    const polarChartVar = new Chart(polarChart, {
      type: 'polarArea',
      data: {
        labels: ['Admin', 'User', 'Patient', 'Doctor'],
        datasets: [
          {
            label: 'Population (millions)',
            backgroundColor: [purpleColor, yellowColor, orangeColor,cyanColor],
            data: data.UserCounts,
            borderWidth: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 500
        },
        scales: {
          r: {
            ticks: {
              display: false,
              color: labelColor
            },
            grid: {
              display: false
            }
          }
        },
        plugins: {
          tooltip: {
            // Updated default tooltip UI
            rtl: isRtl,
            backgroundColor: cardColor,
            titleColor: headingColor,
            bodyColor: legendColor,
            borderWidth: 1,
            borderColor: borderColor
          },
          legend: {
            rtl: isRtl,
            position: 'right',
            labels: {
              usePointStyle: true,
              padding: 25,
              boxWidth: 8,
              boxHeight: 8,
              color: legendColor
            }
          }
        }
      }
    });
  }



  // Doughnut Chart
  // --------------------------------------------------------------------

  const doughnutChart = document.getElementById('doughnutChart');
  if (doughnutChart) {
    const doughnutChartVar = new Chart(doughnutChart, {
      type: 'doughnut',
      data: {
        labels: ['متاح', 'غير متاح'],
        datasets: [
          {
            data: data.Diseases,
            backgroundColor: [cyanColor, config.colors.primary],
            borderWidth: 0,
            pointStyle: 'rectRounded'
          }
        ]
      },
      options: {
        responsive: true,
        animation: {
          duration: 500
        },
        cutout: '68%',
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.labels || '',
                  value = context.parsed;
                const output = ' ' + label + ' : ' + value + ' %';
                return output;
              }
            },
            // Updated default tooltip UI
            rtl: isRtl,
            backgroundColor: cardColor,
            titleColor: headingColor,
            bodyColor: legendColor,
            borderWidth: 1,
            borderColor: borderColor
          }
        }
      }
    });
  }
}

