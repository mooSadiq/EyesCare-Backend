import {fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


/**
 * Displays the patient's profile information on the page.
 */
const isFileCheckbox = document.getElementById('edit-research-switch');
const fileField = document.getElementById('file-input');
const urlField = document.getElementById('url-input');

function showResearchDetails(data) {

  document.getElementById('research-id').innerText = data.research.id;
  document.getElementById('research-title').innerText = data.research.title;
  document.getElementById('research-author').innerText = data.research.authors;
  document.getElementById('research-abstract').innerText = data.research.abstract;
  document.getElementById('research-journal').innerText = data.research.journal_name;
  document.getElementById('research-publicate-date').innerText = data.research.publication_date;
  document.getElementById('research-field').innerText = data.research.field_name;
  document.getElementById('research-institution').innerText = data.research.institution;
  document.getElementById('research-views-count').innerText = data.research.views_count;
  document.getElementById('research-downloads-count').innerText = data.research.downloads_count;
  document.getElementById('research-user-name').innerText = data.research.user_name;
  const avatarElement = document.getElementById('user-avatar');
  // Check if the user has a profile picture, otherwise set a default image
  if (data.research.profile_picture) {
      avatarElement.src = data.research.profile_picture;
  } else {
      avatarElement.src = '/static/img/avatars/avatar-unknown.jpg';
  }
  const researchLinkElement = document.getElementById('research-link');
  const iconElement = document.getElementById('icon-type');
  
  const journalSelect = document.getElementById('edit-research-select-journal');
  initializeSelectData(data.journal, journalSelect);
  const fieldSelect = document.getElementById('edit-research-select-field');
  initializeSelectData(data.field, fieldSelect);


  // Update the edit form fields with user data
  document.getElementById('edit-research-title').value = data.research.title;
  document.getElementById('edit-research-authors').value = data.research.authors;
  document.getElementById('edit-research-abstract').value = data.research.abstract;
  document.getElementById('edit-research-date').value = data.research.publication_date;
  document.getElementById('edit-research-institution').value = data.research.institution;
  document.getElementById('edit-research-select-journal').value = data.research.journal_id;
  document.getElementById('edit-research-select-field').value = data.research.field_id;

  
  const isFile = data.research.is_file;
  isFileCheckbox.checked = isFile;
  console.log(isFile);
  const urlInput = document.getElementById('edit-research-url');
  fileField.style.display = 'none';
  
  if (isFile) {
    fileField.style.display = 'block';  // Show the file input
    urlField.style.display = 'none'; 
    iconElement.className = "ti ti-pdf ti-sm me-2";  // تعيين أيقونة PDF
    researchLinkElement.href = data.research.file;    // Hide the URL input
  } else {
    fileField.style.display = 'none';   // Hide the file input
    urlField.style.display = 'block';
    iconElement.className = "ti ti-link ti-sm me-2";  // تعيين أيقونة الرابط
    researchLinkElement.href = data.research.url;
    urlInput.value = data.research.url;
    console.log(data.research.url);
  }
}

function initializeSelectData(data, element){
  element.innerHTML = ''; // Clear existing options to avoid duplication
  data.forEach(field => {
      const option = document.createElement('option');
      option.value = field.id;
      option.textContent = field.name;
      element.appendChild(option);      
  });
}
/**
 * Fetches patient profile data and initializes the profile display.
 */
async function fetchAndInitializeData() {
  const url_get_research_details_data = `/researches/list/${getId}/`;
  try {
    const data = await fetchAllData(url_get_research_details_data);
    showResearchDetails(data);
  } catch (error) {
    console.error('خطأ في جلب بيانات :', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function(){  
  fetchAndInitializeData();

  isFileCheckbox.addEventListener('change', function() {
    if (isFileCheckbox.checked) {
      fileField.style.display = 'block';  // Show the file input
      urlField.style.display = 'none';    // Hide the URL input
    } else {
      fileField.style.display = 'none';   // Hide the file input
      urlField.style.display = 'block';   // Show the URL input
    }
  });
});
/**
 * Handles the submission of the edit user form, updating the  data.
 */
document.getElementById('editResearchForm').addEventListener('submit', async function (event) {
  event.preventDefault();
      const formData = new FormData();
      formData.append('title', document.getElementById('edit-research-title').value);
      formData.append('abstract', document.getElementById('edit-research-abstract').value);
      formData.append('authors', document.getElementById('edit-research-authors').value);
      formData.append('publication_date', document.getElementById('edit-research-date').value);
      formData.append('journal', document.getElementById('edit-research-select-journal').value);
      formData.append('field', document.getElementById('edit-research-select-field').value);
      formData.append('institution', document.getElementById('edit-research-institution').value);
      const is_file = document.getElementById('edit-research-switch').checked;  
      formData.append('is_file', is_file ? '1' : '0');
      if(is_file) {
        const upload = document.getElementById('edit-research-file').files[0];
        if (upload) {
          formData.append('file', upload);
          formData.append('url', '');
        }
      }
      else {
        formData.append('url', document.getElementById('edit-research-url').value);
        formData.append('file', '');
      }
      
      const method = 'PUT';
      const url = `/researches/list/update/${getId}/`;
      try {
        const result = await submitRequest(url, method, formData );        
        if (result.success) {
          const modalElement = document.getElementById('editResearchModal');
          const modal = bootstrap.Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          }
          showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
          fetchAndInitializeData();
          this.reset();
        }
        else {
          showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }
});

/**
 * Handles the activation or deactivation of the user account.
 */
$(document).on('click', '#confirm-delete', async function () {
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
    const method = 'DELETE';
    const url = `/researches/list/delete/${getId}/`;
    const activeResult = await submitRequest(url, method);
    if(activeResult.success) {
      fetchAndInitializeData();
      showAlert('success',  activeResult.data.is_active ? 'تم التنشيط!' : 'تم إلغاء التنشيط!', activeResult.message, 'btn btn-success');
    }
    else {
      showAlert('error', 'حدث خطأ!', activeResult.message, 'btn btn-danger');
    }
  }
});







