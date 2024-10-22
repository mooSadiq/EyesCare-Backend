from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .models import Disease
from .serializers import DiseasesSerializer, DiseaseTrySerializer
from rest_framework.response import Response
from rest_framework import status
import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import json

# Create your views here.

def diseases_list(request):
    return render(request, 'diseases_list.html')

def diseases_details(request,pk):
    return render(request, 'diseases_details.html',{{"desease_id": pk}})

def edit_diseases_details(request,pk):
    return render(request, 'edit-diseases-details.html',{{'desease_id ':pk}})
def try_diseases(request):
    return render(request, 'try.html')

#Return All Diseases From DB
@api_view(['GET'])
def get_all_diseases(request):
    diseases=Disease.objects.all()
    serializer=DiseasesSerializer(diseases,many=True)
    if serializer.data:
        return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)

#Return one Disease From DB by id
@api_view(['GET'])
def get_disease_by_id(request,pk):
    disease=get_object_or_404(Disease,id=pk)
    serializer=DiseasesSerializer(disease,many=False)
    if serializer.data:
        return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)

#جلب مرض عن طريق الأسم
@api_view(['GET'])
def get_all_diseases_byname(request,nameresartch):
    nameresartch = nameresartch.strip()
    disease=Disease.objects.filter(name=nameresartch)
    serializer=DiseasesSerializer(disease,many=False)
    if serializer.data:
        return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def set_diseas(request):
    disease=Disease.objects.filter(name=request.data['name'])
    if disease.exists():
        return Response({"Info":"This Diseas is already exists"})
    else:
        data=request.data
        print(data)
        Disease.objects.create(
            name_ar=data["name"],
            description_ar=data["description"],
            image=data["image"],
            causes_ar=data["causes"],
            symptoms_ar=data["symptoms"],
            diagnosis_methods_ar=data["diagnosis_methods"],
            treatment_options_ar=data["treatment_options"],
            prevention_recommendations_ar=data["prevention_recommendations"]
        )
        return Response({"message":"تم إضافة المرض بنجاح"},status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_disease(request, pk):
    disease = get_object_or_404(Disease, id=pk)
    serializer = DiseasesSerializer(disease, many=False)
    if not serializer.data:
        return Response({"message": "لايوجد اي مرض"}, status=status.HTTP_404_NOT_FOUND)
    disease.name = request.data.get("name", disease.name)
    disease.description = request.data.get("description", disease.description)
    disease.causes = request.data.get("causes", disease.causes)
    disease.symptoms = request.data.get("symptoms", disease.symptoms)
    disease.diagnosis_methods = request.data.get("diagnosis_methods", disease.diagnosis_methods)
    disease.treatment_options = request.data.get("treatment_options", disease.treatment_options)
    disease.prevention_recommendations = request.data.get("prevention_recommendations", disease.prevention_recommendations)
    if "image" in request.FILES:
        old_image_path = disease.image.path if disease.image else None
        disease.image = request.FILES["image"]
        if old_image_path and os.path.isfile(old_image_path):
            os.remove(old_image_path)
    disease.save()
    return Response({"message": "تم تحديث المرض بنجاح"}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_diseases(request,pk):
    disease=get_object_or_404(Disease,id=pk)
    serializer=DiseasesSerializer(disease,many=False)
    if not serializer.data:
        return Response({"message":"لم يتم إيجاد المرض"},status=status.HTTP_404_NOT_FOUND)
    else:
        result=disease.delete()
        if result:
            return Response({"message":"تم الحذف بنجاح!"},status=status.HTTP_200_OK)
        else:
            return Response({"message":" لم يتم الحذف "},status=status.HTTP_200_OK)

class DiseaseCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        print(data)
        # التأكد من أن الحقول JSON تُمرر كقواميس
        # لا حاجة لاستخدام json.loads هنا إذا كانت الحقول بالفعل قواميس
        # فقط تأكد من أن الحقول موجودة
        causes_ar = data.get('causes_ar', {})
        causes_en = data.get('causes_en', {})
        symptoms_ar = data.get('symptoms_ar', {})
        symptoms_en = data.get('symptoms_en', {})
        diagnosis_methods_ar = data.get('diagnosis_methods_ar', {})
        diagnosis_methods_en = data.get('diagnosis_methods_en', {})
        treatment_options_ar = data.get('treatment_options_ar', {})
        treatment_options_en = data.get('treatment_options_en', {})
        prevention_recommendations_ar = data.get('prevention_recommendations_ar', {})
        prevention_recommendations_en = data.get('prevention_recommendations_en', {})
        
        # إدخال البيانات في النموذج
        try:
            disease = Disease(
                name_ar=data['name_ar'],
                name_en=data['name_en'],
                description_ar=data['description_ar'],
                description_en=data['description_en'],
                causes_ar=causes_ar,  # استخدم القاموس مباشرة
                causes_en=causes_en,
                symptoms_ar=symptoms_ar,
                symptoms_en=symptoms_en,
                diagnosis_methods_ar=diagnosis_methods_ar,
                diagnosis_methods_en=diagnosis_methods_en,
                treatment_options_ar=treatment_options_ar,
                treatment_options_en=treatment_options_en,
                prevention_recommendations_ar=prevention_recommendations_ar,
                prevention_recommendations_en=prevention_recommendations_en,
                status=data['status']
            )
            disease.save()
            return Response({"message": "تم إدخال البيانات بنجاح", "data": data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
class DiseaseTryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        diseases = Disease.objects.all()
        serializer = DiseaseTrySerializer(diseases, many=True, context={'request': request})
        
        response_data = {
            "status": True,
            "code": 200,
            "message": "ok",
            "data": serializer.data
        }

        return Response(response_data)