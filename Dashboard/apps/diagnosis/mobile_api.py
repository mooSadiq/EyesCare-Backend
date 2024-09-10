from django.http import JsonResponse
from django.shortcuts import render
import os
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from .models import MyModel  # استيراد النموذج الذي يحتوي على حقل الملف
from inference_sdk import InferenceHTTPClient

@method_decorator(csrf_exempt, name='dispatch')
class ImageInferenceView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)

        my_model_instance = MyModel(title="My Image", image=image)
        my_model_instance.save()

        saved_image_path = my_model_instance.image.path


        client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="Mw0WRYo7QKz4vlBJWxWG"
        )
        
        result = client.infer(saved_image_path, model_id="alltheimaegs/1")
        
        if result:
            predictions = result.get('predictions', [])
            if predictions:
              class_value = predictions[0].get('class')
              if class_value == 'normal':
                  diagnosis_data = {
                        'diagnosis_status': 'لا توجد مشاكل ظاهرة',
                        'message': 'تحليل الصورة يظهر أن العين سليمة ولا توجد مشاكل ظاهرة. لكن إذا كنت تشعر بأي ألم أو أعراض، نوصي بزيارة طبيب العيون للاطمئنان. صحتك تهمنا!',
                    }
                  return JsonResponse({
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'تم العثور على نتيجة',
                    'data': diagnosis_data
                  })
              else:
                  diagnosis_data = {
                        'disease_id': 1,
                        'diagnosis_status': class_value,
                        'message': 'يرجى ملاحظة أن هذه النتائج ليست تشخيصًا نهائيًا. نوصي بزيارة طبيب عيون مختص للحصول على تقييم دقيق وموثوق والحصول على الرعاية الصحية اللازمة.',
                        }
                  return JsonResponse({
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'تم العثور على نتيجة',
                    'data': diagnosis_data
                  })
            else:
                diagnosis_data = {
                        'diagnosis_status': 'لم يتم العثور على نتيجة ',
                        'message': 'عذرًا، لم نتمكن من تشخيص الحالة بدقة. قد تكون الصورة غير واضحة أو الحالة غير مدرجة ضمن قائمة الأمراض التي يمكننا اكتشافها. يرجى إعادة المحاولة بصورة أوضح أو استشارة طبيب عيون للحصول على تشخيص دقيق.',
                        }
                return JsonResponse({
                        'status': True,
                        'code': status.HTTP_200_OK,
                        'message': 'لم يتم العثور على نتيجة ',
                        'data': diagnosis_data
                })
        else:
            return JsonResponse({
                      'status': False,
                      'code': status.HTTP_404_NOT_FOUND,
                      'message': 'فشل',
            })

