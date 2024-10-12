from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .models import Disease
from .serializers import DiseasesSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import os
# Create your views here.

def diseases_list(request):
    return render(request, 'diseases_list.html')

def diseases_details(request,pk):
    return render(request, 'diseases_details.html',{{"desease_id": pk}})

def edit_diseases_details(request,pk):
    return render(request, 'edit-diseases-details.html',{{'desease_id ':pk}})

#Return All Diseases From DB
class DiseasesList(APIView):
    def get(self,request):
        permission_classes=[IsAuthenticated]
        diseases=Disease.objects.all()
        serializer=DiseasesSerializer(diseases,many=True)
        if serializer.data:
            return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
        else :
            return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)

#Return one Disease From DB by id
class DiseasList(APIView):
    def get(self,request,pk):
        permission_classes=[IsAuthenticated]
        disease=get_object_or_404(Disease,id=pk)
        serializer=DiseasesSerializer(disease,many=False)
        if serializer.data:
            return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
        else :
            return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)


class DiseasesSet(APIView):
    def post(self,request):
        disease=Disease.objects.filter(name_en=request.data['name_en'])
        if disease.exists():
            return Response({"Info":"This Diseas is already exists"})
        else:
            data=request.data
            Disease.objects.create(
                name_ar=data["name_ar"],
                name_en=data["name_en"],
                description_ar=data["description_ar"],
                description_en=data["description_en"],
                image=data["image"],
                causes_ar=data["causes_ar"],
                causes_en=data["causes_en"],
                symptoms_ar=data["symptoms_ar"],
                symptoms_en=data["symptoms_en"],
                diagnosis_methods_ar=data["diagnosis_methods_ar"],
                diagnosis_methods_en=data["diagnosis_methods_en"],
                treatment_options_ar=data["treatment_options_ar"],
                treatment_options_en=data["treatment_options_en"],
                prevention_recommendations_ar=data["prevention_recommendations_ar"],
                prevention_recommendations_en=data["prevention_recommendations_en"],
                status=data["status"]
            )
            return Response({"message":"تم إضافة المرض بنجاح"},status=status.HTTP_201_CREATED)

class DiseaseUpdate(APIView):
    def put(self,request, pk):
        disease = get_object_or_404(Disease, id=pk)
        serializer = DiseasesSerializer(disease, many=False)
        if not serializer.data:
            return Response({"message": "لايوجد اي مرض"}, status=status.HTTP_404_NOT_FOUND)
        disease.name_ar = request.data.get("name_ar", disease.name_ar)
        disease.name_en = request.data.get("name_en", disease.name_en)
        disease.description_ar = request.data.get("description_ar", disease.description_ar)
        disease.description_en = request.data.get("description_en", disease.description_en)
        disease.causes_ar = request.data.get("causes_ar", disease.causes_ar)
        disease.causes_en = request.data.get("causes_en", disease.causes_en)
        disease.symptoms_ar = request.data.get("symptoms_ar", disease.symptoms_ar)
        disease.symptoms_en = request.data.get("symptoms_en", disease.symptoms_en)
        disease.diagnosis_methods_ar = request.data.get("diagnosis_methods_ar", disease.diagnosis_methods_ar)
        disease.diagnosis_methods_en = request.data.get("diagnosis_methods_en", disease.diagnosis_methods_en)
        disease.treatment_options_ar = request.data.get("treatment_options_ar", disease.treatment_options_ar)
        disease.treatment_options_en = request.data.get("treatment_options_en", disease.treatment_options_en)
        disease.prevention_recommendations_ar = request.data.get("prevention_recommendations_ar", disease.prevention_recommendations_ar)
        disease.prevention_recommendations_en = request.data.get("prevention_recommendations_en", disease.prevention_recommendations_en)
        disease.status = request.data.get("status", disease.status)
        if "image" in request.FILES:
            old_image_path = disease.image.path if disease.image else None
            disease.image = request.FILES["image"]
            if old_image_path and os.path.isfile(old_image_path):
                os.remove(old_image_path)
        disease.save()
        return Response({"message": "تم تحديث المرض بنجاح"}, status=status.HTTP_200_OK)

class DiseasesDelete(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk):
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

