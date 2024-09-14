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
        alert(error);
        console.error(`خطأ في جلب بيانات التشخيصات باستخدام ID: ${diagnosis_Id}`, error);
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
        const image = diagnosis.image;
        const completed = diagnosis.compeleted;

        const disease = diagnosis.disease;
        const patient = diagnosis.patient.user;

        //ملئ أماكن البيانات
        //بيانات التشخيص 
        document.getElementById('diagnosis-id').innerText = diagnosis.id;
        document.getElementById('diagnosis_image').src = diagnosis.image;
        document.getElementById('diagnosis_date').innerText = diagnosis.diagnosis_date;
        document.getElementById('diagnosis_result').innerText = diagnosis.diagnosis_result;
        document.getElementById('disease_description').innerText = disease.description;
        //بيانات المريض الشخصية
        document.getElementById('patient_name').innerText = patient.first_name +" "+ patient.last_name;
        document.getElementById('patient_email').innerText = patient.email;

        //بيانات المرض
        document.getElementById('disease_causes').innerText = disease.causes;
        document.getElementById('disease_symptoms').innerText = disease.symptoms;
        document.getElementById('diagnosis_methods').innerText = disease.diagnosis_methods;
        document.getElementById('treatment_options').innerText = disease.treatment_options;
        document.getElementById('prevention_recommendations').innerText = disease.prevention_recommendations;
       

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

  // Alert With Functional Confirm Button حذف
//   const confirmText = document.querySelector('#confirm-text');
//   confirmText.onclick = function () {
//     Swal.fire({
//       title: 'هل أنت متأكد؟',
//       icon: 'warning',
//       showCancelButton: true,
//       confirmButtonText: 'نعم !',
//       CancelButtonText: 'الغاء',
//       customClass: {
//         confirmButton: 'btn btn-primary me-3 ',
//         cancelButton: 'btn btn-label-secondary '
//       },
//       buttonsStyling: false
//     }).then(function (result) {
//       if (result.value) {
//         Swal.fire({
//           icon: 'success',
//           title: 'تم الحذف!',
//           text: 'لقد تم حذف التشخيص بنجاح.',
//           customClass: {
//             confirmButton: 'btn btn-success '
//           }
//         });
//       }
//     });
//   };