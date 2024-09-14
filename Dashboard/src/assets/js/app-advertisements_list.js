import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';



// دالة لجلب بيانات الاعلانات من API

async function fetchAdvertisementsData() {
    const url_get_advertisements_data = '/advertisements/api/getaDvertisements/';
    try {
        const data = await fetchAllData(url_get_advertisements_data);
        updateAdvertisementsData(data);
    } catch (error) {

        console.error('خطأ في جلب بيانات الاعلانات:', error);
    }


}


//دالة عرض نافذة التعديل
function setupEditModal(advertisement) {
    // تعيين القيم إلى عناصر HTML داخل النافذة المنبثقة
    document.getElementById('exampleFormControlTextarea1').value = advertisement.about;
    document.getElementById('switch-input-verified').checked = advertisement.allowed;


    // تعيين معرّف الإعلان في النافذة المنبثقة (لإرساله لاحقًا عبر API)
    document.getElementById('modalCenter').setAttribute('data-ad-id', advertisement.id);
}
//انتهاء دالة عرض النافذة للتعديل

//ارسال البيانات للتعديل عبر API //////////
document.querySelector('.save-update').onclick = async function () {
    const adId = document.getElementById('modalCenter').getAttribute('data-ad-id');
    const aboutText = document.getElementById('exampleFormControlTextarea1').value;
    const allowed = document.getElementById('switch-input-verified').checked ? true : false;
    const imageInput = document.getElementById('modalEditUserFile');

    // إعداد FormData لتحميل البيانات والصورة
    const formData = new FormData();
    formData.append('about', aboutText);
    formData.append('allowed', allowed);

    // التحقق من وجود صورة جديدة وتحميلها إذا كانت موجودة
    if (imageInput.files[0]) {
        formData.append('ad_image', imageInput.files[0]);
    }

    try {
        const response = await submitRequest(`/advertisements/api/update/${adId}/`, 'PATCH', formData, {
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.success) {
            console.error('Error response:', response);
            alert('حدث خطأ أثناء حفظ التعديلات.');
        } else {
            Swal.fire({
                icon: 'success',
                title: 'تم الحفظ!',
                text: 'تم تحديث البيانات بنجاح',
                customClass: {
                    confirmButton: 'btn btn-success'
                }
            });
            fetchAdvertisementsData();
        }
    } catch (error) {
        console.error('Error during fetch operation:', error);
        alert('حدث خطأ أثناء حفظ التعديلات.');
    }

    // إغلاق الفورم بعد الإضافة
    const modalElement = document.getElementById('modalCenter');
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide();
    }
};



//انتهاء دالة ارسال البيانات بعد التعديل وتحديث الصفحة

// دالة تحديث البيانات وجلبها وعرضها 
function updateAdvertisementsData(data) {

    let adv_count = 0;
    let adv_views_counts = 0;
    let adv_clicks_counts = 0;

    if (data.advertisement && data.advertisement.length > 0) {


        const advertisementsContainer = document.getElementById('advertisementsContainer');
        advertisementsContainer.innerHTML = ''; // تفريغ المحتوى الحالي
        data.advertisement.forEach((advertisement) => {
            // احصائيات اعلى الجدول
            adv_count++;
            adv_views_counts += advertisement.views_count;
            adv_clicks_counts += advertisement.clicks_count;
            document.getElementById('advrtisement_count').innerText = adv_count;
            document.getElementById('advrtisement_views_count').innerText = adv_views_counts;
            document.getElementById('advrtisement_clicks_count').innerText = adv_clicks_counts;

            const adCard = document.createElement('div');
            adCard.className = 'col-sm-6 col-lg-4';

            // تحديد تواريخ البداية والنهاية
            const start_date = new Date(advertisement.start_date);
            const end_date = new Date(advertisement.end_date);
            const current_date = new Date();

            // التحقق من حالة الإعلان وتحديد العنصر المناسب
            let statusElement;
            if (current_date < start_date) {
                statusElement = `<a class="btn btn-label-warning d-flex align-items-center" href="javascript:;">
                                    <span class="me-2">قيد الانتظار</span>
                                    <i class="ti ti-clock-play ti-sm"></i>
                                </a>`;
            } else if (current_date >= start_date && current_date <= end_date) {
                statusElement = `<a class="btn btn-label-success d-flex align-items-center" href="javascript:;">
                                    <span class="me-2">نشط</span>
                                    <i class="ti ti-activity ti-sm"></i>
                                </a>`;
            } else {
                statusElement = `<a class="btn btn-label-primary d-flex align-items-center" href="javascript:;">
                                    <span class="me-2">منتهي</span>
                                    <i class="ti ti-square-check ti-sm"></i>
                                </a>`;
            }

            // تحديد الصورة اذا تم العثور عليها في قاعدة البيانات والا عرض صورة اعلان عامة
            let adImg = advertisement.ad_image;
            if (adImg == null) {
                adImg = "/media/ads/advertisement.png";
            }

            // إضافة عنصر "محظور" إذا كان الإعلان غير مسموح له بالظهور
            const specialOfferRibbon = advertisement.allowed ? '' : `
                <a href="javascript:;" class="special-offer-ribbon btn-label-warning py-1 position-absolute" style="top: 0; right: 0; transform: rotate(45deg);">
                    محظور
                </a>`;

            // بناء محتوى الإعلان بناءً على القالب المقدم
            adCard.innerHTML = `
                <div class="card p-2 h-55 shadow-none border position-relative">
                    ${specialOfferRibbon}
                   <div class="ad-card rounded-2 text-center mb-2">
                      <a href="javascript:;">
                             <img class="img-fluid ad-img" src="${adImg}" alt="advertisement image">
                    </a>
                </div>

                    <div class="card-body p-3 pt-2 text-center">
                        <div class="d-flex justify-content-around align-items-center mb-1">
                            <h6 class="d-flex align-items-center justify-content-center gap-1 mb-0">
                                <span class="text-muted">${advertisement.views_count}</span>
                                <span class="text"><i class="ti ti-eye me-1 mt-n1"></i></span>
                            </h6>
                            <h6 class="d-flex align-items-center justify-content-center gap-1 mb-0">
                                <span class="text-muted">${advertisement.clicks_count}</span>
                                <span><i class="ti ti-hand-click me-1 mt-n1"></i></span>
                            </h6>
                        </div>
                        <a href="${advertisement.ad_link}" class="h6">${advertisement.advertiser}</a>
                        <div class="date d-flex align-items-center mt-2">
                            <i class="ti ti-clock me-2 mb-3"></i>
                            <p class="start_date">${advertisement.start_date}</p>
                            <p class="mx-1"> - </p>
                            <p class="end_date">${advertisement.end_date}</p>
                        </div>
                        <div class="d-flex justify-content-center gap-2 text-nowrap text-center">
                            <a class="btn btn-label-danger delete-advertisement" href="javascript:;" type="button" data-id="${advertisement.id}">
                                <i class="ti ti-trash align-middle"></i>
                            </a>
                            <a class="btn btn-label-primary edit-advertisement" href="javascript:;" type="button" data-bs-toggle="modal" data-bs-target="#modalCenter">
                                <i class="ti ti-edit align-middle"></i>
                            </a>
                            <div class="adStatus">${statusElement}</div>
                        </div>
                    </div>
                </div>
            `;

            // إضافة عنصر الإعلان الجديد إلى حاوية الإعلانات
            if (advertisementsContainer) {
                advertisementsContainer.appendChild(adCard);
            } else {
                console.error('advertisementsContainer is not defined or not found.');
            }

            // إعداد النافذة المنبثقة عند النقر على زر التحرير
            adCard.querySelector('.edit-advertisement').onclick = function () {
                setupEditModal(advertisement);
            };
        });


    }
}
// دالة حذف إعلان

$(document).on('click', '.delete-advertisement', async function () {
    const advertisementId = $(this).data('id');
    const result = await showConfirmationDialog();
    if (result.isConfirmed) {
        const method = 'DELETE';
        const url = `/advertisements/api/delete/advertisement/${advertisementId}/`;
        const deleteResult = await submitRequest(url, method);

        if (deleteResult.success) {
            showAlert('success', 'تم الحذف!', deleteResult.message, 'btn btn-success');
            fetchAdvertisementsData();
        } else {
            showAlert('error', 'حدث خطأ!', deleteResult.message, 'btn btn-danger');
        }
    }
});

//دالة إضافة إعلان
// اضافة إعلان
document.getElementById('addNewAdvertidementForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    // الحصول على القيم من الحقول المدخلة
    const phone_number = document.getElementById('add-advertiser-phoneNumber').value;
    const imageInput = document.getElementById('modalEditUserFile');
    const advertiser = document.getElementById('add-advertiser-fullname').value;
    const ad_link = document.getElementById('add-link').value;
    const advertisement_text = document.getElementById('advertisement-text').value;
    const start_date = document.getElementById('start-date').value;
    const end_date = document.getElementById('end-date').value;

    const formData = new FormData();
    formData.append('advertiser', advertiser);
    formData.append('ad_link', ad_link);
    formData.append('phone_number', phone_number);
    formData.append('start_date', start_date);
    formData.append('end_date', end_date);
    formData.append('status', 1);
    formData.append('about', advertisement_text);

    // التحقق من وجود صورة جديدة وتحميلها إذا كانت موجودة
    if (imageInput.files[0]) {
        formData.append('ad_image', imageInput.files[0]);
    }

    const method = 'POST';
    const url = '/advertisements/api/createAdvertisement/';

    try {
        const result = await submitRequest(url, method, formData, {});

        if (result.success) {
            const offcanvasElement = document.getElementById('offcanvasAddAdvertisement');
            const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
            if (offcanvas) {
                offcanvas.hide();
            }
            showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
            fetchAdvertisementsData();
            this.reset();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error adding advertisement:', error);
    }
});


document.addEventListener('DOMContentLoaded', fetchAdvertisementsData);

