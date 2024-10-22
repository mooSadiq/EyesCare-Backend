from datetime import datetime
import os
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from .models import DiagnosisReport, Disease, MyModel
# from apps.patients.models import Patient
# from .serializers import (
#     DiagnosisSerializer,
#     DiagnosisSerializerDash,
# )
# from rest_framework.views import APIView
# from .Eye_Diseases_Detect import disease_detect
# from urllib.parse import urljoin


def index(request):
    return render(request, "diagnosis_list.html")


def diagnosisDetails(request, id):
    return render(request, "diagnosis_details.html", {"diagnosis_id": id})


def diagnosisDetailsPrint(request):
    return render(request, "diagnosis_details_print.html")


# def detect_Eye(image_path):

#     image, label, confidence = Eye_Diseases_Detect.disease_detect(image_path)
#     if image is not None:  #  أي اذا كانت عين
#         return image, label
#     elif confidence is not None:
#         return image_path, label
#     elif label == "No Diseases detected.":
#         return image_path, label
#     #  else:
#     #    return None, "تأكد من التقاط الصورة بشكل مناسب"
#     elif image is None:
#         if label == "No eye detected in the image.":
#             label = "يبدو أن الصورة ليست عين! "
#         elif label == "The model did not find a confident prediction.":
#             label = "الصورة غير واضحة، اجلب صورة أوضح"
#         elif label == "Error during RobowFlow inference hint:'Check Internet'.":
#             label = "تحقق من الاتصال بالانترنت!"
#         elif label == "No Diseases detected.":
#             label = "عذراً، لم نتمكن من اكتشاف هذا المرض!"

#         return None, label


# class DisagnosisListView(APIView):
#     def get(self, request):
#         diagnosis = DiagnosisReport.objects.all()
#         diagnosis_serializer = DiagnosisSerializerDash(diagnosis, many=True)
#         return Response(
#             {"diagnosis": diagnosis_serializer.data}, status=status.HTTP_200_OK
#         )

#     def delete(self, request, pk):
#         try:
#             diagnoses = DiagnosisReport.objects.filter(pk=pk)[0]
#             if not diagnoses:
#                 return Response(
#                     {"success": False, "message": "التشخيص غير موجود"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#             diagnoses.delete()
#             return Response(
#                   {"success": True, "message": "تم حذف التشخيص بنجاح"},
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response(
#                 {"error": True, "message": f"لم يتم الحذف بسبب مشكلة: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

# # # # دلة تشخيص صورة
# @method_decorator(csrf_exempt, name="dispatch")
# class ImageUploadView(APIView):
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
#                     "success": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "الصورة ليست صورة عبن",
#                 }
#             )
#         elif label == "The model did not find a confident prediction.":
#             return JsonResponse(
#                 {
#                     "success": False,
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
#                     "success": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "تصنيف غير مدرج",
#                 }
#             )
#         elif detected_image != None:
#             domain = request.get_host()
#             image_path = urljoin(f"http://{domain}", detected_image)
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
#                     "success": True,
#                     "code": status.HTTP_200_OK,
#                     "message": "تم العثور على نتيجة",
#                     "disease_type": label,
#                 }
#             )
#         elif detected_image == None and conf != None:
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
#                     "success": True,
#                     "code": status.HTTP_200_OK,
#                     "message": "تم العثور على نتيجة ",
#                     "disease_type": label,
#                 }
#             )
#         else:
#             return JsonResponse(
#                 {
#                     "label": label,
#                     "success": False,
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "فشل",
#                 }
#             )


# def generate_image_name(original_name):
#     # الحصول على الوقت الحالي بصيغة يمكن قراءتها
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#     # الحصول على الامتداد من الاسم الأصلي
#     _, extension = os.path.splitext(original_name)

#     # توليد اسم جديد يتضمن الوقت الحالي
#     new_image_name = f'{"image_"}{timestamp}{extension}'

#     return new_image_name


# # جلب بيانات التقرير
# class ReportDiagnosisView(APIView):
#     def get(self, request, pk):
#         try:
#             # الحصول على تقرير التشخيص باستخدام المعرف المقدم
#             report = get_object_or_404(DiagnosisReport, id=pk)
#             diagnosis_serializer = DiagnosisSerializer(report)

#             # إرجاع استجابة JSON تحتوي على بيانات التقرير كاملة
#             return JsonResponse(
#                 {"diagnosis": diagnosis_serializer.data}, status=status.HTTP_200_OK
#             )

#         except Http404:
#             # إرجاع رسالة خطأ عند عدم العثور على التقرير أو المرض
#             return JsonResponse(
#                 {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             # إرجاع رسالة خطأ عامة في حالة حدوث استثناء آخر
#             return JsonResponse(
#                 {"error": "gggg"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
