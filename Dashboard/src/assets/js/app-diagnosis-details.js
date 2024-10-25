import { fetchAllData, submitRequest } from './api.js';
import { showAlert, showConfirmationDialog } from './general-function.js';


/**
 * Page diagnoses details
 */

'use strict'

// الدالة الرئيسية التي يتم استعداؤها تلقائيا عند فتح الصفحة
$(function () {

    fetchAndInitializeTable(diagnosisId);


});

//دالة جلب البيانات عن طريقapi

async function fetchAndInitializeTable(diagnosis_Id) {
    const url_get_diagnosis_details = `/diagnosis/api/report/details/${diagnosis_Id}/`;
    try {
        const data = await fetchAllData(url_get_diagnosis_details);
        updateDiagnosisDetail(data);
    } catch (error) {
        console.error(`خطأ في جلب بيانات التشخيصات باستخدام ID: ${diagnosis_Id}`, error);
    }
}

function makelist(text,elem) {
    const lines = text.split(',');
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

//دالة عرض البيانات على وسط صفحة التطبيق
function updateDiagnosisDetail(data) {
    // alert(data)
    // التحقق من وجود الكائن diagnosis في البيانات
    if (data && data.diagnosis) {
        const diagnosis = data.diagnosis;

        // استخراج القيم المطلوبة
        const diagnosisResult = diagnosis.diagnosis_result;
        const diagnosisDate = diagnosis.diagnosis_date;
        let image = diagnosis.image;
        image = image.replace('/media/media/', '/media/');
        const patient = diagnosis.patient;
        const completed = diagnosis.compeleted;
        const disease = diagnosis.disease;
        //بيانات المريض الشخصية
        document.getElementById('patient_name').innerText = patient.first_name +" "+ patient.last_name;
        document.getElementById('patient_email').innerText = patient.email;

        //ملئ أماكن البيانات
        //بيانات التشخيص
        document.getElementById('diagnosis-id').innerText = diagnosis.id;
        document.getElementById('diagnosis_image').src = image;
        document.getElementById('diagnosis_date').innerText = diagnosis.diagnosis_date;
        document.getElementById('diagnosis_result').innerText = diagnosis.diagnosis_result;
        document.getElementById('confidence').innerText = diagnosis.confidence;
        document.getElementById('disease_description').innerText = disease.description;

        //بيانات المرض
        document.getElementById('disease_description').innerText = disease.description_ar;
        let dataCausesList = disease.causes_points_ar;
        let CousesList = document.getElementById('disease_causes');
        document.getElementById('disease_causes_p').innerText = disease.causes_paragraph_ar;
        makelist(dataCausesList, CousesList);

        let dataSympthomsList = disease.symptoms_points_ar;
        let sympthomsList = document.getElementById('disease_symptoms');
        document.getElementById('disease_symptoms_p').innerText = disease.symptoms_paragraph_ar;
        makelist(dataSympthomsList, sympthomsList);

        let dataDiagnosisMethodsList = disease.diagnosis_methods_points_ar;
        let diagnosisMethodsList = document.getElementById('diagnosis_methods');
        document.getElementById('diagnosis_methods_p').innerText = disease.diagnosis_methods_paragraph_ar;
        makelist(dataDiagnosisMethodsList, diagnosisMethodsList);

        let dataTreatementOptionsList = disease.treatment_options_points_ar;
        let TreatementOptionsList = document.getElementById('treatment_options');
        document.getElementById('treatment_options_p').innerText = disease.treatment_options_paragraph_ar
        makelist(dataTreatementOptionsList, TreatementOptionsList);

        let dataPreventionRecommendationsList = disease.prevention_recommendations_points_ar;
        let PreventionRecommendationsList = document.getElementById('prevention_recommendations');
        document.getElementById('prevention_recommendations_p').innerText = disease.prevention_recommendations_paragraph_ar;
        makelist(dataPreventionRecommendationsList, PreventionRecommendationsList);

    }

}

//طباعة التقرير
(function () {
    //دالة تعمل على طباعة التقرير بتحديد العناصر المراد طباعتها واخفاء البقية
    $("#printButton").click(function() {
      // إخفاء العناصر التي لا نريد طباعتها
      $(".hide-print").hide();
      // إضافة كلاس shadow-none حتى يتم اخفاء ظل العناثر في الملف المطبوع
      $(".diagnosis-preview-card").addClass("shadow-none");

      //  طباعة الصفحة
      window.print();

      // إزالة كلاس shadow-none وإعادة عرض العناصر المخفية
      $(".diagnosis-preview-card").removeClass("shadow-none");
      $(".hide-print").show();
    });



  })();

