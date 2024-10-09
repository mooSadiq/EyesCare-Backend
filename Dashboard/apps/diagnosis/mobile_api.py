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
from . import Detect_Eye
from .Eye_Diseases_Detect import disease_detect
from urllib.parse import urljoin

@method_decorator(csrf_exempt, name='dispatch')
class ImageInferenceView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)

        my_model_instance = MyModel(title="My Image", image=image)
        my_model_instance.save()

        saved_image_path = my_model_instance.image.path
        detected_image,label,conf=disease_detect(saved_image_path)
        # {
        #     image,classfication_label,Confidence
        #     None, "No eye detected in the image.",None
        #     None, "The model did not find a confident prediction.",None
        #     None, "Error during RobowFlow inference hint:'Check Internet'.",None
        #     None, "No Diseases detected.",None
        #     None, Internal_Disease_classfication_label,Confidence
        # }
        
        if detected_image != None:
            domain = request.get_host()
            image_path=urljoin(f'http://{domain}', detected_image)
            diagnosis_data = {
                            'image_path':image_path,
                            'diagnosis_status': label,
                            'confidence':conf,
                            'message': 'يرجى ملاحظة أن هذه النتائج ليست تشخيصًا نهائيًا. نوصي بزيارة طبيب عيون مختص للحصول على تقييم دقيق وموثوق والحصول على الرعاية الصحية اللازمة.',
                            }
            return JsonResponse({
                        'status': True,
                        'code': status.HTTP_200_OK,
                        'message': 'تم العثور على نتيجة',
                        'data': diagnosis_data
                        })
        elif detected_image == None and conf != None:
                    diagnosis_data = {
                            'diagnosis_status': label,
                            'confidence':conf,
                            'message': 'يرجى ملاحظة أن هذه النتائج ليست تشخيصًا نهائيًا. نوصي بزيارة طبيب عيون مختص للحصول على تقييم دقيق وموثوق والحصول على الرعاية الصحية اللازمة.',
                            }
                    return JsonResponse({
                            'status': True,
                            'code': status.HTTP_200_OK,
                            'message': 'تم العثور على نتيجة ',
                            'data': diagnosis_data
                    })
        elif label=="No eye detected in the image.":
            return JsonResponse({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'الصورة ليست صورة عبن',
            })
        elif label=="The model did not find a confident prediction.":
            return JsonResponse({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': ' قم بإرسال الصورة مرة أخرى لم يتم التعرف عليها' ,
            })
        elif label=="No Diseases detected.":
            return JsonResponse({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'تصنيف غير مدرج' ,
            })
        else:
                return JsonResponse({
                        'label':label,
                        'status': False,
                        'code': status.HTTP_404_NOT_FOUND,
                        'message': 'فشل',
            })


