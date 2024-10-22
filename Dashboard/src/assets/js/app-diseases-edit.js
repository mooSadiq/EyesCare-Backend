import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


let diseaseId;
function showDiseasesDetails(data) {
    diseaseId=data.id;
    document.getElementById('diseasename').value = data.name_ar;
    document.getElementById('diseasenameen').value = data.name_en;
    document.getElementById('diseaseDescription').value = data.description_ar;
    document.getElementById('diseaseDescriptionen').value = data.description_en;
    document.getElementById('diseaseCauses').value = data.causes_paragraph_ar;
    document.getElementById('diseaseCausesen').value = data.causes_points_en;
    document.getElementById('diseaseCausespoints').value = data.causes_points_ar;
    document.getElementById('diseaseCausesenpoints').value = data.causes_points_en;
    document.getElementById('diseaseSymptoms').value = data.symptoms_paragraph_ar;
    document.getElementById('diseaseSymptomsen').value = data.symptoms_paragraph_en;
    document.getElementById('diseaseSymptomspoints').value = data.symptoms_points_ar;
    document.getElementById('diseaseSymptomsenpoints').value = data.symptoms_points_en;
    document.getElementById('diseaseDiagnosis').value = data.diagnosis_methods_paragraph_ar;
    document.getElementById('diseaseDiagnosisen').value = data.diagnosis_methods_paragraph_en;
    document.getElementById('diseaseDiagnosispoints').value = data.diagnosis_methods_points_ar;
    document.getElementById('diseaseDiagnosisenpoints').value = data.diagnosis_methods_points_en;
    document.getElementById('diseaseTreatment').value = data.treatment_options_paragraph_ar;
    document.getElementById('diseaseTreatmentpoints').value = data.treatment_options_points_ar;
    document.getElementById('diseaseTreatmenten').value = data.treatment_options_paragraph_en;
    document.getElementById('diseaseTreatmentenpoints').value = data.treatment_options_points_en;
    document.getElementById('diseasePrevention').value = data.prevention_recommendations_paragraph_ar;
    document.getElementById('diseasePreventionen').value = data.prevention_recommendations_paragraph_en;
    document.getElementById('diseasePreventionpoints').value = data.prevention_recommendations_points_ar;
    document.getElementById('diseasePreventionenpoints').value = data.prevention_recommendations_points_en;
    document.getElementById('imagePreview').value = data.image;
    document.getElementById('status').value = data.status;
}
/**
 * Fetches Diseases Details data and initializes the profile display.
 */
async function fetchAndInitializeData() {
        const url_get_diseases_details_data = `/diseases/api/get/all/diseasebyid/${getId2}/`;
        try {
        const data = await fetchAllData(url_get_diseases_details_data);
        console.log(data)
        showDiseasesDetails(data.Diseases);
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
    const formData = new FormData(this);
    const method = 'PUT';
    const url = `/diseases/api/update/disease/${diseaseId}/`;
    const imageFile = formData.get('image');
    if (!imageFile || imageFile.size === 0) {
        formData.delete('image'); // حذف الصورة من البيانات المرسلة
    }

    try {
        const result = await submitRequest(url, method, formData);
        if (result.success) {
            window.location.href = '/diseases/';
            showAlert('success', 'تم الحفظ!', result.message, 'btn btn-success');
            fetchAndInitializeData();
            this.reset();
        } else {
            showAlert('error', 'فشل الحفظ!', result.message, 'btn btn-error');
        }
    } catch (error) {
        console.error('Error updating data:', error);
    }
});
