from datetime import datetime
import os
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import DiagnosisReport, Disease, mymodel
from apps.patients.models import Patient

from .serializers import DiagnosisSerializer, DiseaseSerializer, ImageUploadSerializer
from config import settings

from apps.doctor.models import Doctor
from apps.users.models import CustomUser

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from inference_sdk import InferenceHTTPClient
from . import Detect_Eye

# Create your views here.
# إعداد عميل Roboflow
# CLIENT = InferenceHTTPClient(
#     api_url="https://detect.roboflow.com",
#     api_key="Mw0WRYo7QKz4vlBJWxWG"
# )

def index(request):
  return render(request, 'diagnosis_list.html')

def diagnosisDetails(request, id):
  return render(request, 'diagnosis_details.html', {"diagnosis_id": id})

def diagnosisDetailsPrint(request):
  return render(request, 'diagnosis_details_print.html')



# هذي الدالة الي توصل لل module
def detect_Eye():
    result = Detect_Eye.classify_and_save_image(image_path='1.jpg')
    print(result)

# result شكل النتائج 
# {
#     "Eye",
#     "Internal-Eye",
#     "No detection: No eye detected",
#     "No sufficient confidence."
# }

#اعداد رابط ارسال الصورة الى المودل
client = InferenceHTTPClient(
                api_url="https://detect.roboflow.com",
                api_key=settings.ROBOFLOW_API_KEY
            )
#جلب بيانات التشخيصات
class DisagnosisListView(APIView):
  def get(self, request):
        diagnosis = DiagnosisReport.objects.all()
        diagnosis_serializer = DiagnosisSerializer(diagnosis, many=True)
        return Response({'diagnosis': diagnosis_serializer.data}, status=status.HTTP_200_OK)
      
  def delete(self, request, pk):
        # جلب التشخيص المحدد باستخدام المعرف (pk)
        diagnosis = get_object_or_404(DiagnosisReport, pk=pk)
        
        # حذف التشخيص
        diagnosis.delete()
        
        # إرجاع استجابة تأكيدية بنجاح الحذف
        return Response({'success': True, 'message': 'تشخيص تم حذفه بنجاح'}, status=status.HTTP_200_OK)
# دلة تشخيص صورة
# @method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': 'لا توجد صورة'}, status=400)

        new_name = generate_image_name(image.name)
        
        print(image.name)
        image.name = new_name
        print(image.name)
        #جلب كائن المريض من جدول المرضى
        patient = get_object_or_404(Patient, id=2) 
        # حفظ الملف بشكل دائم في قاعدة البيانات
        my_model_instance = mymodel(title="MyImage", image=image)
        my_model_instance.save()

        # مسار الملف المحفوظ بشكل دائم
        saved_image_path = my_model_instance.image.path
        print(saved_image_path)
        
        disease = get_object_or_404(Disease, id=1)
        disease_type = "unknown"
        completed = False
        try:
          
            
            # تمرير مسار الملف المحفوظ بشكل دائم إلى infer
            response = client.infer(saved_image_path, model_id="alltheimaegs/1")
            
            if response:
                predictions = response.get('predictions', [])
                
                for prediction in predictions:
                  disease_type = prediction.get('class')

                if disease_type == "unknown":
                   completed = False
                else:
                  completed = True
                # حفظ التشخيص في قاعدة البيانات
                
                diagnosis_report = DiagnosisReport(
                   diagnosis_result=disease_type,
                  image = saved_image_path,
                  compeleted= completed,
                  patient= patient,
                 disease = disease
                )
                diagnosis_report.save()

                return JsonResponse({"message":' نتيجة التشخيص هي: '+ disease_type,
                                     'disease_type':disease_type})
            else:
                return JsonResponse({'failed': 'عذراً، لم يتم التعرف على المرض!' + disease_type, 'disease_type':disease_type} )
        
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
          

def generate_image_name(original_name):
    # الحصول على الوقت الحالي بصيغة يمكن قراءتها
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # الحصول على الامتداد من الاسم الأصلي
    _, extension = os.path.splitext(original_name)
    
    # توليد اسم جديد يتضمن الوقت الحالي
    new_image_name = f'{"image_"}{timestamp}{extension}'
    
    return new_image_name
# جلب بيانات التقرير
class ReportDiagnosisView(APIView):
    def get(self, request, pk):
        try:
            # الحصول على تقرير التشخيص باستخدام المعرف المقدم
            report = get_object_or_404(DiagnosisReport, id=pk)
            diagnosis_serializer = DiagnosisSerializer(report)
            
        
            
            # إرجاع استجابة JSON تحتوي على بيانات التقرير كاملة
            return JsonResponse({'diagnosis': diagnosis_serializer.data}, status=status.HTTP_200_OK)

        # except Http404:
        #     # إرجاع رسالة خطأ عند عدم العثور على التقرير أو المرض
        #     return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # إرجاع رسالة خطأ عامة في حالة حدوث استثناء آخر
            return JsonResponse({'error': 'gggg'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
