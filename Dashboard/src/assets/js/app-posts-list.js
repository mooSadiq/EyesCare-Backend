import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';

'use strict';

let currentPage = 1;  
async function fetchDisplayPosts(page, searchQuery) {
        const year = document.getElementById('yearFilter').value;
        const month = document.getElementById('monthFilter').value;
        const image = document.getElementById('imageFilter').value;
        const dateOrder = document.getElementById('dateOrder').value;
        const interactionOrder = document.getElementById('interactionOrder').value;
        const viewsOrder = document.getElementById('viewsOrder').value;

        const dateOrderParam = dateOrder === 'desc' ? '-created_at' : 'created_at';
        const interactionOrderParam = interactionOrder === 'most' ? '-likes_count' : 'likes_count';
        const viewsOrderParam = viewsOrder === 'most' ? '-views_count' : 'views_count';
        const url = new URL('/posts/api/get/posts/', window.location.origin);
        console.log(window.location.origin); 
        url.searchParams.append('page', page);
        if (searchQuery) url.searchParams.append('search', searchQuery);
        if (year) url.searchParams.append('year', year);
        if (month) url.searchParams.append('month', month);
        if (image) url.searchParams.append('image', image);
        if (dateOrder) url.searchParams.append('date_order', dateOrderParam);
        if (interactionOrder) url.searchParams.append('interaction_order', interactionOrderParam);
        if (viewsOrder) url.searchParams.append('views_order', viewsOrderParam);

    try {
        const data = await fetchAllData(url);

        const postsCount = document.getElementById('posts-count');
        postsCount.innerHTML = data.results.total_posts_count; 
        const container = document.getElementById('posts-container');
        container.innerHTML = ''; 
        console.log(data);
        data.results.posts.forEach(post => {
            const post_detail_url = `/posts/details/`; 
            const postHTML = `
                <div class="col-sm-6 col-lg-4">
                    <div class="card p-2 h-70 shadow-none border">
                        <div class="rounded-2 text-center mb-2">
                            <a href="${post_detail_url}">
                                <img
                                    class="img-fluid"
                                    src="${post.image_url ? post.image_url : '/static/img/pages/no-image.jpg'}"
                                    alt="Post image"
                                    style="
                                        width: 100%;
                                        height: 150px;
                                        object-fit: cover;
                                        border-radius: 8px;
                                    "
                                />
                            </a>
                        </div>
                        <div class="card-body p-3 pt-2">
                            <div class="d-flex justify-content-around align-items-center mb-1">
                                <h6 class="d-flex align-items-center justify-content-center gap-1 mb-0">
                                    <span class="text-muted">${post.views_count}</span>
                                    <span class="text"><i class="ti ti-eye me-1 mt-n1"></i></span>
                                </h6>
                                <h6 class="d-flex align-items-center justify-content-center gap-1 mb-0">
                                    <span class="text-muted">${post.likes_count}</span>
                                    <span class="text-danger"><i class="ti ti-heart-filled me-1 mt-n1"></i></span>
                                </h6>
                            </div>
                            <a href="${post_detail_url}" class="h6">${post.name}</a>
                            <p class="mt-2 postBody" style="
                                overflow: hidden; 
                                text-overflow: ellipsis; 
                                display: -webkit-box; 
                                -webkit-line-clamp: 2;
                                -webkit-box-orient: vertical; 
                                line-height: 1.5em;
                                height: 3em; 
                            ">${post.text}</p>
                            <p class="d-flex align-items-center">
                                <i class="ti ti-clock me-2 mt-n1"></i>
                                ${post.created_at}
                            </p>
                            <div class="d-flex flex-column flex-md-row gap-2 text-nowrap">
                                <a
                                    class="app-post-md-50 btn btn-label-danger me-md-2 d-flex align-items-center delete-post"
                                    href="javascript:;"
                                    data-id="${post.post_id}"
                                    type="button" id="confirm-text">
                                    <span>حذف</span>
                                    <i class="ti ti-trash align-middle me-2 mt-n1 ti-sm"></i>
                                </a>
                                <a
                                    class="app-post-md-50 btn btn-label-primary d-flex align-items-center"
                                    href="${post_detail_url}">
                                    <span class="me-2">التفاصيل</span>
                                    <i class="ti ti-list-details ti-sm"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>`;
            
            container.innerHTML += postHTML;
        });
        updatePagination(data.links, data.total_pages, searchQuery);
    } catch (error) {
        console.error('خطأ في جلب المنشورات:', error);
    }
}

function updatePagination(links, totalPages, searchQuery) {
  const paginationContainer = document.getElementById('pagination');
  paginationContainer.innerHTML = '';

  paginationContainer.innerHTML += `
      <li class="page-item prev ${!links.previous ? 'disabled' : ''}">
          <a class="page-link" href="javascript:void(0);" data-page="${currentPage - 1}">
              <i class="ti ti-chevron-left ti-xs scaleX-n1-rtl"></i>
          </a>
      </li>`;

  for (let i = 1; i <= totalPages; i++) {
      paginationContainer.innerHTML += `
          <li class="page-item ${i === currentPage ? 'active' : ''}">
              <a class="page-link" href="javascript:void(0);" data-page="${i}">${i}</a>
          </li>`;
  }

  paginationContainer.innerHTML += `
      <li class="page-item next ${!links.next ? 'disabled' : ''}">
          <a class="page-link" href="javascript:void(0);" data-page="${currentPage + 1}">
              <i class="ti ti-chevron-right ti-xs scaleX-n1-rtl"></i>
          </a>
      </li>`;

  document.querySelectorAll('.page-link').forEach(link => {
      link.addEventListener('click', function () {
          const page = parseInt(this.getAttribute('data-page'), 10);
          if (!isNaN(page)) {
            currentPage = page;
            fetchDisplayPosts(currentPage, searchQuery);
          }
      });
  });
}
document.getElementById('searchInput').addEventListener('input', function() {
  const searchQuery = this.value;
  fetchDisplayPosts(currentPage, searchQuery);
});


document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  let searchQuery = searchInput.value || '';

  function updatePosts() {
    fetchDisplayPosts(currentPage, searchQuery);
  }

  fetchDisplayPosts(currentPage, searchQuery);

  document.getElementById('searchButton').addEventListener('click', function() {
    searchQuery = searchInput.value;
    updatePosts();
  });

  document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      searchQuery = this.value;
      updatePosts();
    }
  });

  document.getElementById('searchInput').addEventListener('input', function() {
    searchQuery = this.value;
    updatePosts();
  });

  function handleFilterChange() {
    searchQuery = searchInput.value;
    updatePosts();
  }

  document.getElementById('yearFilter').addEventListener('change', handleFilterChange);
  document.getElementById('monthFilter').addEventListener('change', handleFilterChange);
  document.getElementById('imageFilter').addEventListener('change', handleFilterChange);
  document.getElementById('dateOrder').addEventListener('change', handleFilterChange);
  document.getElementById('interactionOrder').addEventListener('change', handleFilterChange);
  document.getElementById('viewsOrder').addEventListener('change', handleFilterChange);
});




/**
 * Handles the submission of the 'Add New User' form.
 * This function validates the form, sends a POST request to add a new user,
 * and updates the DataTable with the newly added user.
 */
document.getElementById('addNewPostForm').addEventListener('submit', async function (event) {
  event.preventDefault();

  const formData = new FormData();
  formData.append('text', document.getElementById('add-post-text').value);

  // Check if a profile picture is uploaded, and add it to the form data
  const upload = document.getElementById('add-post-image').files[0];
  if (upload) {
      formData.append('image', upload);
  }

  
  const method = 'POST';
  const url = '/posts/api/create/';
  try {
    const result = await submitRequest(url, method, formData );
    if (result.success) {
      const offcanvasElement = document.getElementById('offcanvasAddPost');
      const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
      if (offcanvas) {
        offcanvas.hide();  
      }
      showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
      fetchDisplayPosts(currentPage);
      this.reset();
    } else {
      showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
    }
  } catch (error) {
    console.error('Error adding user:', error);
  }
  });


/**
 * Handles the deletion of a post when the delete button is clicked.
 * This function prompts the user for confirmation and sends a DELETE request to the server.
 * Upon successful deletion, it updates the DataTable to reflect the change.
 */

$(document).on('click', '.delete-post', async function () {
  const postId = $(this).data('id');
  const result = await showConfirmationDialog();
  if (result.isConfirmed) {
    const method = 'DELETE';
    const url = `/posts/api/delete/${postId}/`;
    const deleteResult = await submitRequest(url, method, null);

    if (deleteResult.success) {
      showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
      fetchDisplayPosts(currentPage);
  } else {
      showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
  }
  }
});