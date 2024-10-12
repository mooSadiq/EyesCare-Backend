# # from datetime import datetime
# # import os
# # from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
# # from django.views import View
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view,permission_classes
# # from rest_framework import status
# # from django.utils.decorators import method_decorator
# # from django.views.decorators.csrf import csrf_exempt

# # from .models import DiagnosisReport, Disease, MyModel
# # from apps.patients.models import Patient

# # from .serializers import DiagnosisSerializer, DiseaseSerializer, ImageUploadSerializer
# # from config import settings

# # from apps.doctor.models import Doctor
# # from apps.users.models import CustomUser

# # from rest_framework.views import APIView
# # from rest_framework.permissions import IsAuthenticated

# # from inference_sdk import InferenceHTTPClient
# # from . import Detect_Eye
# # from . import Eye_Diseases_Detect


def index(request):
  return render(request, 'diagnosis_list.html')

def diagnosisDetails(request, id):
  return render(request, 'diagnosis_details.html', {"diagnosis_id": id})

def diagnosisDetailsPrint(request):
  return render(request, 'diagnosis_details_print.html')



# # # هذي الدالة الي توصل لل module
# #  # detected_image,label=disease_detect(saved_image_path)
# #         # {
# #         #     image,classfication_label,Confidence
# #         #     None, "No eye detected in the image.",None
# #         #     None, "The model did not find a confident prediction.",None
# #         #     None, "Error during RobowFlow inference hint:'Check Internet'.",None
# #         #     None, "No Diseases detected.",None
# #         #     None, Internal_Disease_classfication_label,Confidence
# #         # }
# # def detect_Eye(image_path):
    
# #      image, label,confidence  = Eye_Diseases_Detect.disease_detect(image_path)
# #      if image is not None:  #  أي اذا كانت عين
# #         return image,label
# #      elif confidence is not None:
# #          return image_path, label
# #     #  else:
# #     #    return None, "تأكد من التقاط الصورة بشكل مناسب"
# #      elif image is None:
# #        if label == "No eye detected in the image.":
# #          label = "يبدو أن الصورة ليست عين! "
# #        elif label == "The model did not find a confident prediction.":
# #          label = "الصورة غير واضحة، اجلب صورة أوضح"
# #        elif label == "Error during RobowFlow inference hint:'Check Internet'.":
# #          label = "تحقق من الاتصال بالانترنت!"
# #        elif label == "No Diseases detected.":
# #          label = "عذراً، لم نتمكن من اكتشاف هذا المرض!"
       
# #        return None, label
    

# # # result شكل النتائج 
# # # {
# # #     "Eye",
# # #     "Internal-Eye",
# # #     "No detection: No eye detected",
# # #     "No sufficient confidence.",
# # #      "Error during RobowFlow inference hint:'Check Internet'."
# # # }

# # #اعداد رابط ارسال الصورة الى المودل
# # client = InferenceHTTPClient(
# #                 api_url="https://detect.roboflow.com",
# #                 api_key=settings.ROBOFLOW_API_KEY
# #             )
# # #جلب بيانات التشخيصات
# # class DisagnosisListView(APIView):
# #   def get(self, request):
# #         diagnosis = DiagnosisReport.objects.all()
# #         diagnosis_serializer = DiagnosisSerializer(diagnosis, many=True)
# #         return Response({'diagnosis': diagnosis_serializer.data}, status=status.HTTP_200_OK)
      
# #   def delete(self, request, pk):
# #         # جلب التشخيص المحدد باستخدام المعرف (pk)
# #         diagnosis = get_object_or_404(DiagnosisReport, pk=pk)
        
# #         # حذف التشخيص
# #         diagnosis.delete()
        
# #         # إرجاع استجابة تأكيدية بنجاح الحذف
# #         return Response({'success': True, 'message': 'تشخيص تم حذفه بنجاح'}, status=status.HTTP_200_OK)
# # # دلة تشخيص صورة
# # @method_decorator(csrf_exempt, name='dispatch')
# class ImageUploadView(APIView):
#     def post(self, request, *args, **kwargs):
# #         image = request.FILES.get('image')
# #         if not image:
# #             return JsonResponse({'error': 'لا توجد صورة'}, status=400)

# #         new_name = generate_image_name(image.name)
        
# #         print(image.name) #قابل للحذف
# #         image.name = new_name 
# #         print(image.name) #قابل للحذف
# #         #جلب كائن المريض من جدول المرضى
# #         patient = get_object_or_404(Patient, id=2) #قابل للحذف
# #         # patient = request.user
# #         # حفظ الملف بشكل دائم في قاعدة البيانات
# #         my_model_instance = MyModel(title="MyImage", image=image)
# #         my_model_instance.save()

# #         # مسار الملف المحفوظ بشكل دائم
# #         saved_image_path = my_model_instance.image.path
# #         print(saved_image_path) #قابل للحذف
        
# #         # disease = get_object_or_404(Disease, id=1) #قابل للحذف
        
# #         disease_type = "unknown"
# #         completed = False
# #         try:
          
            
# #             # تمرير مسار الملف المحفوظ بشكل دائم إلى infer
# #             # response = client.infer(saved_image_path, model_id="alltheimaegs/1")
# #             # response = client.infer(saved_image_path, model_id="ccatract/4")
# #             # هنا يقوم ابستدعاء الدالة لتقوم بالكشف عن العين والتشخيص 
# #             img, label = detect_Eye(saved_image_path)
# #             if img is not None:
# #               if label == "No Diseases detected.": # اذا لم يتم تحديد المرض
# #                  disease_type= "unknown" # يتم تخزينه على انه غير معرف
# #               else: #واذا تم تحديده نأخذ اسمه
# #                 disease = Disease.objects.get(name_en=label)
# #                 disease_type =disease.name_ar
# #                 print("label: ", label) #قابل للحذف
            
            
              
            
# #             # if response:
# #             #     predictions = response.get('predictions', [])
                
# #             #     for prediction in predictions:
# #             #       disease_type = prediction.get('class')
# #                 # يتم حذف الكود السابق الاربعة الاسطر والمواصلة من هنا
# #               if disease_type == "unknown":
# #                  completed = False
# #               else:
# #                   completed = True
                  
# #                 # حفظ التشخيص في قاعدة البيانات
# #               diagnosis_report = DiagnosisReport(
# #                    diagnosis_result=disease_type,
# #                   image = saved_image_path,
# #                   compeleted= completed,
# #                   patient= patient,
# #                  disease = disease
# #                 )
# #               diagnosis_report.save()
# #               #هنا اذا تم التعرف على العين يعيد نتيجة التشخيص اما اسم المرض بالعربي ااو unknown
# #               return JsonResponse({"success":True, "message":' نتيجة التشخيص هي: '+ disease_type,
# #                                      'disease_type':disease_type})
# #             else:
# #                 # return JsonResponse({"success":False,'message': 'عذراً، يبدوا أن الصورة التي تم ارسالها ليست صورة عين!'} )
# #                 return JsonResponse({"success":False,'message': label} )
        
# #         except Exception as e:
# #             return JsonResponse({'message': str(e)}, status=500)
             

# # def generate_image_name(original_name):
# #     # الحصول على الوقت الحالي بصيغة يمكن قراءتها
# #     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
# #     # الحصول على الامتداد من الاسم الأصلي
# #     _, extension = os.path.splitext(original_name)
    
# #     # توليد اسم جديد يتضمن الوقت الحالي
# #     new_image_name = f'{"image_"}{timestamp}{extension}'
    
# #     return new_image_name
# # # جلب بيانات التقرير
# # class ReportDiagnosisView(APIView):
# #     def get(self, request, pk):
# #         try:
# #             # الحصول على تقرير التشخيص باستخدام المعرف المقدم
# #             report = get_object_or_404(DiagnosisReport, id=pk)
# #             diagnosis_serializer = DiagnosisSerializer(report)
            
        
            
# #             # إرجاع استجابة JSON تحتوي على بيانات التقرير كاملة
# #             return JsonResponse({'diagnosis': diagnosis_serializer.data}, status=status.HTTP_200_OK)

# #         # except Http404:
# #         #     # إرجاع رسالة خطأ عند عدم العثور على التقرير أو المرض
# #         #     return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

# #         except Exception as e:
# #             # إرجاع رسالة خطأ عامة في حالة حدوث استثناء آخر
# #             return JsonResponse({'error': 'gggg'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
