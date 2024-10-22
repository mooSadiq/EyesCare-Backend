import {fetchAllData, submitRequest } from './api.js';


function makelist(text,elem) {
    const lines = text;
    if (elem) {
        elem.innerHTML = '';
        lines.forEach(line => {
            if (line.trim() !== '') {
                const li = document.createElement('li');
                li.textContent = line;
                li.classList.add("mb-1");
                elem.appendChild(li);
            }
        });
    } else {
        console.error('العنصر ذو المعرف "couseslist" غير موجود في الصفحة.');
    }
}

let diseaseId;
function showDiseasesDetails(data) {
    diseaseId = data.id;
    document.getElementById('diseases-desc').innerText = data.description_ar;
    let dataCausesList = data.causes.points;
    let CousesList = document.getElementById('couseslist');
    document.getElementById('couses-p').innerText = data.causes.paragraph;
    makelist(dataCausesList, CousesList);

    let dataSympthomsList = data.symptoms.points;
    let sympthomsList = document.getElementById('sympthomslist');
    document.getElementById('sympthoms-p').innerText = data.symptoms.paragraph;
    makelist(dataSympthomsList, sympthomsList);

    let dataDiagnosisMethodsList = data.diagnosis_methods.points;
    let diagnosisMethodsList = document.getElementById('diagnosisMethodslist');
    document.getElementById('diagnosisMethods-p').innerText = data.diagnosis_methods.paragraph;
    makelist(dataDiagnosisMethodsList, diagnosisMethodsList);

    let dataTreatementOptionsList = data.treatment_options.points;
    let TreatementOptionsList = document.getElementById('treatementoptionslist');
    document.getElementById('treatementoptions-p').innerText = data.treatment_options.paragraph;
    makelist(dataTreatementOptionsList, TreatementOptionsList);

    let dataPreventionRecommendationsList = data.prevention_recommendations.points;
    let PreventionRecommendationsList = document.getElementById('preventionrecommendationslist');
    document.getElementById('preventionrecommendations-p').innerText = data.prevention_recommendations.paragraph;
    makelist(dataPreventionRecommendationsList, PreventionRecommendationsList);

    const diseasesImage = document.getElementById('diseases-image');
    if (data.image) {
        diseasesImage.src = data.image;
    } else {
        diseasesImage.src = "malek";
    }

    document.getElementById('editButton').addEventListener('click', function() {
        window.location.href = `/diseases/edit_details/${diseaseId}/`;
    });
}




/**
 * Fetches patient profile data and initializes the profile display.
 */
async function fetchAndInitializeData() {
        console.log(`Mallllllek${getId}`)
        const url_get_diseases_details_data = `/diseases/api/get/diseasebyid/${getId}/`;
        try {
        const data = await fetchAllData(url_get_diseases_details_data);
        showDiseasesDetails(data.Diseases);
        } catch (error) {
        console.error('خطأ في جلب بيانات المرض:', error);
        }
    }

document.addEventListener('DOMContentLoaded', fetchAndInitializeData);
