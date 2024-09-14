from django.http import JsonResponse
from django.shortcuts import render
import os
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

        # حفظ الملف بشكل دائم في قاعدة البيانات
        my_model_instance = MyModel(title="My Image", image=image)
        my_model_instance.save()

        # مسار الملف المحفوظ بشكل دائم
        saved_image_path = my_model_instance.image.path

        try:
            client = InferenceHTTPClient(
                api_url="https://detect.roboflow.com",
                api_key="Mw0WRYo7QKz4vlBJWxWG"
            )
            
            # تمرير مسار الملف المحفوظ بشكل دائم إلى `infer`
            result = client.infer(saved_image_path, model_id="alltheimaegs/1")
            
            if result:
                data = result
                class_id_value = data['predictions'][0]['class']
                print(class_id_value)
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Error with the API call'}, status=500)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def index(request):
  return render(request, 'diagnosis_list.html')

def diagnosisDetails(request):
  return render(request, 'diagnosis_details.html')

def diagnosisDetailsPrint(request):
  return render(request, 'diagnosis_details_print.html')