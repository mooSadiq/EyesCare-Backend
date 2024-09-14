import {fetchAllData, submitRequest } from './api.js';


function makelist(text,elem) {
    const lines = text.split('\r\n');
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
    diseaseId=data.id;
    document.getElementById('diseases-desc').innerText=data.description;
    dataCouseslist=data.causes;
    CousesList=document.getElementById('couseslist');
    makelist(dataCouseslist,CousesList);
    dataSympthomsList=data.sympthoms;
    sympthomsList=document.getElementById('sympthomslist');
    makelist(dataSympthomsList,sympthomsList);
    dataDiagnosisMethodsList=data.diagnosis_methods;
    diagnosisMethodsList=document.getElementById('diagnosisMethodslist');
    makelist(dataDiagnosisMethodsList,diagnosisMethodsList);
    dataTreatementOptionsList=data.treatement_options;
    TreatementOptionsList=document.getElementById('treatementoptionslist');
    makelist(dataTreatementOptionsList,TreatementOptionsList);
    dataPreventionRecommendationsList=data.prevention_recommendations;
    PreventionRecommendationsList=document.getElementById('preventionrecommendationslist');
    makelist(dataPreventionRecommendationsList,PreventionRecommendationsList);
    const diseasesImage = document.getElementById('diseases-image');
    // Check if the user has a profile picture, otherwise set a default image
    if (data.image) {
        diseasesImage.src = data.image;
    }
    document.getElementById('editButton').addEventListener('click', function() {
        window.location.href = `/diseases/edit_details/${diseaseId}/`;
    });
}





/**
 * Fetches patient profile data and initializes the profile display.
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
