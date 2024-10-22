# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from apps.diseases.models import Disease
# from apps.patients.models import Patient
# from .models import MyModel, DiagnosisReport  # استيراد النموذج الذي يحتوي على حقل الملف
# from .Eye_Diseases_Detect import disease_detect
# from urllib.parse import urljoin
# from rest_framework.views import APIView
# from .serializers import DiagnosisSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class ImageInferenceView(APIView):
#     disease_label = {
#         "stey": "Stye",
#         "catract": "Cataracts",
#         "DR": "Diabetic Retinopathy",
#         "Glaucoma": "Glaucoma",
#         "RVO": "Retinal Vein Occlusion",
#         "pterygium": "Pterygium",
#         "conjunctivitis": "Conjunctivitis",
#         "Cataract": "Cataracts",
#     }

#     def post(self, request, *args, **kwargs):
#         image = request.FILES.get("image")
#         if not image:
#             return JsonResponse({"error": "No image provided"}, status=400)
#         my_model_instance = MyModel(title="My Image", image=image)
#         my_model_instance.save()
#         saved_image_path = my_model_instance.image.path
#         saved_image_path_report=my_model_instance.image.url
#         detected_image, label, conf = disease_detect(my_model_instance.image)
#         if request.user.user_type != "doctor" and request.user.user_type != "admin":
#             patient, created = Patient.objects.get_or_create(user=request.user)
#             if created:
#                 request.user.user_type = "patient"
#                 request.user.save()
#         if label == "No eye detected in the image.":
#             return JsonResponse(
#                 {
#                     "status": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "الصورة ليست صورة عبن",
#                 }
#             )
#         elif label == "The model did not find a confident prediction.":
#             return JsonResponse(
#                 {
#                     "status": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": " قم بإرسال الصورة مرة أخرى لم يتم التعرف عليها",
#                 }
#             )
#         elif label == "No Diseases detected.":
#             DiagnosisReport.objects.create(
#                 diagnosis_result="unkown",
#                 image=saved_image_path_report,
#                 compeleted=False,
#                 patient=request.user,
#             )
#             return JsonResponse(
#                 {
#                     "status": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "تصنيف غير مدرج",
#                 }
#             )
#         elif detected_image != None:
#             domain = request.get_host()
#             image_path = urljoin(f"http://{domain}", detected_image)
#             diagnosis_data = {
#                 "image_path": image_path,
#                 "diagnosis_status": label,
#                 "confidence": conf,
#                 "message": "يرجى ملاحظة أن هذه النتائج ليست تشخيصًا نهائيًا. نوصي بزيارة طبيب عيون مختص للحصول على تقييم دقيق وموثوق والحصول على الرعاية الصحية اللازمة.",
#             }
#             if label == "normal":
#                 DiagnosisReport.objects.create(
#                     diagnosis_result="Normal-(طبيعي)",
#                     image=saved_image_path_report,
#                     confidence=conf,
#                     compeleted=True,
#                     patient=request.user,
#                 )
#             else:
#                 Disease_Id = Disease.objects.get(name_en=self.disease_label[label])
#                 DiagnosisReport.objects.create(
#                     diagnosis_result=f"{Disease_Id.name_en}-({Disease_Id.name_ar})",
#                     image=saved_image_path_report,
#                     compeleted=True,
#                     confidence=conf,
#                     patient=request.user,
#                     disease=Disease_Id,
#                 )
#             return JsonResponse(
#                 {
#                     "status": True,
#                     "code": status.HTTP_200_OK,
#                     "message": "تم العثور على نتيجة",
#                     "data": diagnosis_data,
#                 }
#             )
#         elif detected_image == None and conf != None:
#             diagnosis_data = {
#                 "diagnosis_status": label,
#                 "confidence": conf,
#                 "message": "يرجى ملاحظة أن هذه النتائج ليست تشخيصًا نهائيًا. نوصي بزيارة طبيب عيون مختص للحصول على تقييم دقيق وموثوق والحصول على الرعاية الصحية اللازمة.",
#             }
#             if label == "normal":
#                 DiagnosisReport.objects.create(
#                     diagnosis_result="Normal-(طبيعي)",
#                     image=saved_image_path_report,
#                     compeleted=True,
#                     confidence=conf,
#                     patient=request.user,
#                 )
#             else:
#                 Disease_Id = Disease.objects.get(name_en=self.disease_label[label])
#                 DiagnosisReport.objects.create(
#                     diagnosis_result=f"{Disease_Id.name_en}-({Disease_Id.name_ar})",
#                     image=saved_image_path_report,
#                     compeleted=True,
#                     confidence=conf,
#                     patient=request.user,
#                     disease=Disease_Id,
#                 )
#             return JsonResponse(
#                 {
#                     "status": True,
#                     "code": status.HTTP_200_OK,
#                     "message": "تم العثور على نتيجة ",
#                     "data": diagnosis_data,
#                 }
#             )
#         else:
#             return JsonResponse(
#                 {
#                     "label": label,
#                     "status": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "فشل",
#                 }
#             )


# class DiagnosisReportList(APIView):
#         def fix_media_path(self, image_path):
#             parts = image_path.split('media/')
#             if len(parts) > 1:
#                 fixed_path = 'media/' + parts[-1]
#                 return fixed_path

#         def get(self, request):
#                 try:
#                         diagnosisReport = DiagnosisReport.objects.filter(patient=request.user).order_by('-id')
#                         serializer = DiagnosisSerializer(
#                                 diagnosisReport,context={"request": request}, many=True
#                         )
#                         modified_data = []
#                         for x in serializer.data:
#                             original_image_path = x.get('image_path')
#                             fixed_image_path = self.fix_media_path(original_image_path)
#                             modified_report = x.copy()
#                             domain = request.get_host()
#                             image_path = urljoin(f"http://{domain}", fixed_image_path)
#                             modified_report['image_path'] = image_path  # تحديث مسار الصورة
#                             modified_data.append(modified_report)  # إضافة البيانات المعدلة إلى القائمة
#                         if modified_data:
#                                 return Response(
#                                 {
#                                         "status": True,
#                                         "code": 200,
#                                         "message": "لقد تم جلب البيانات بنجاح",
#                                         "data": modified_data,
#                                 },
#                                 status=status.HTTP_200_OK,
#                                 )
#                         else:
#                                 return Response(
#                                 {"status": False, "code": 404, "message": "لا يوجد أي بيانات"},
#                                 status=status.HTTP_404_NOT_FOUND,
#                                 )
#                 except DiagnosisReport.DoesNotExist:
#                         return Response(
#                         {"status": False, "code": 404, "message": "التقرير غير موجود"},
#                         status=status.HTTP_404_NOT_FOUND,
#                         )