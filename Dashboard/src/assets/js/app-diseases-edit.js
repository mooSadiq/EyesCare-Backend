import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


let diseaseId;
function showDiseasesDetails(data) {
    diseaseId=data.id;
    document.getElementById('diseaseName').value = data.name;
    document.getElementById('diseaseDescription').value = data.description;
    document.getElementById('diseaseCauses').value = data.causes;
    document.getElementById('diseaseSymptoms').value = data.sympthoms;
    document.getElementById('diseaseDiagnosis').value = data.diagnosis_methods;
    document.getElementById('diseaseTreatment').value = data.treatement_options;
    document.getElementById('diseasePrevention').value = data.prevention_recommendations;
    document.getElementById('imagePreview').value = data.image;
}
/**
 * Fetches Diseases Details data and initializes the profile display.
 */
async function fetchAndInitializeData() {
        const url_get_diseases_details_data = `/diseases/api/get/diseasebyid/${getId}/`;
        try {
        const data = await fetchAllData(url_get_diseases_details_data);
        showDiseasesDetails(data);
        } catch (error) {
        console.error('خطأ في جلب بيانات المرض:', error);
        }
    }

document.addEventListener('DOMContentLoaded', fetchAndInitializeData);




    /**
     * Handles the submission of the edit Diseases form, updating the Diseases data.
     */
    document.getElementById('diseaseForm').addEventListener('submit', async function (event) {
        event.preventDefault();
            const formData = new FormData();
            formData.append('name', document.getElementById('diseaseName').value);
            formData.append('description', document.getElementById('diseaseDescription').value);
            formData.append('symptoms', document.getElementById('diseaseSymptoms').value);
            formData.append('causes', document.getElementById('diseaseCauses').value);
            formData.append('diagnosis_methods', document.getElementById('diseaseDiagnosis').value);
            formData.append('treatment_options', document.getElementById('diseaseTreatment').value);
            formData.append('prevention_recommendations', document.getElementById('diseasePrevention').value);
            
        // Check if a profile picture is uploaded, and add it to the form data
        const upload = document.getElementById('diseaseImages').files[0];
            if (upload) {
                formData.append('image', upload);
            }
            const method = 'PUT';
            const url = `/diseases/api/update/disease/${diseaseId}/`;
            try {
            const result = await submitRequest(url, method, formData );        
            if (result.success) {
                window.location.href = '/diseases/';
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
















// $(document).ready(function() {
//     $('#editButton').click(function() {
//         $(this).hide();
//         $('#saveButton').show();
//         $('#diseaseForm textarea, #diseaseForm input[type="file"]').prop('readonly', false).prop('disabled', false);
//     });

//     $('#saveButton').click(function() {
//         $(this).hide();
//         $('#editButton').show();
//         $('#diseaseForm textarea, #diseaseForm input[type="file"]').prop('readonly', true).prop('disabled', true);
//         // يمكنك إضافة شفرة لحفظ التعديلات هنا
//         alert('تم حفظ التعديلات');
//     });
   
//     $('#diseaseImages').change(function() {
//         $('#imagePreview').empty();
//         var files = this.files;
//         var preview = $('#imagePreview');
//         if (files.length > 0) {
//             if (files.length == 1) {
//                 preview.addClass('single-image').removeClass('multiple-images');
//             } else {
//                 preview.addClass('multiple-images').removeClass('single-image');
//             }
//             for (var i = 0; i < files.length; i++) {
//                 var file = files[i];
//                 var reader = new FileReader();
//                 reader.onload = function(e) {
//                     var img = $('<img>').attr('src', e.target.result);
//                     preview.append(img);
//                 }
//                 reader.readAsDataURL(file);
//             }
//         }
//     });
// });