from django.shortcuts import render,get_object_or_404
from .models import Disease
from .serializers import DiseaseArabicSerializer,DiseaseAllSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import os

# Create your views here.

def diseases_list(request):
    return render(request, 'diseases_list.html')

def diseases_details(request,pk):
    return render(request, 'diseases_details.html',{"desease_id": pk})

def edit_diseases_details(request,pk):
    return render(request, 'edit-diseases-details.html',{'desease_id':pk})

def try_diseases(request):
    return render(request, 'try.html')

#Return All Diseases From DB
class DiseasesList(APIView):
    def get(self,request):
        permission_classes=[IsAuthenticated]
        diseases=Disease.objects.all()
        serializer=DiseaseArabicSerializer(diseases,many=True,context={'request': request})
        if serializer.data:
            return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
        else :
            return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)

#Return one Disease From DB by id
class DiseasList(APIView):
    def get(self,request,pk):
        permission_classes=[IsAuthenticated]
        disease=get_object_or_404(Disease,id=pk)
        serializer=DiseaseArabicSerializer(disease,many=False,context={'request': request})
        if serializer.data:
            return Response({"Diseases":serializer.data},status=status.HTTP_200_OK)
        else :
            return Response({"Info":"There is not any deases"},status=status.HTTP_404_NOT_FOUND)


class DiseasListall(APIView):
    def get(self,request,pk):
        permission_classes=[IsAuthenticated]
        disease=get_object_or_404(Disease,id=pk)
        serializer=DiseaseAllSerializer(disease,many=False,context={'request': request})
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
            if data["status"]=='true':
                data["status"]=True
            else:
                data["status"]=False
            Disease.objects.create(
                name_ar=data["name_ar"],
                name_en=data["name_en"],
                description_ar=data["description_ar"],
                description_en=data["description_en"],
                image=data["image"],
                causes_paragraph_ar=data["causes_paragraph_ar"],
                causes_points_ar=data["causes_points_ar"],
                causes_paragraph_en=data["causes_paragraph_en"],
                causes_points_en=data["causes_points_en"],
                symptoms_paragraph_ar=data["symptoms_paragraph_ar"],
                symptoms_points_ar=data["symptoms_points_ar"],
                symptoms_paragraph_en=data["symptoms_paragraph_en"],
                symptoms_points_en=data["symptoms_points_en"],
                diagnosis_methods_paragraph_ar=data["diagnosis_methods_paragraph_ar"],
                diagnosis_methods_points_ar=data["diagnosis_methods_points_ar"],
                diagnosis_methods_paragraph_en=data["diagnosis_methods_paragraph_en"],
                diagnosis_methods_points_en=data["diagnosis_methods_points_en"],
                treatment_options_paragraph_ar=data["treatment_options_paragraph_ar"],
                treatment_options_points_ar=data["treatment_options_points_ar"],
                treatment_options_paragraph_en=data["treatment_options_paragraph_en"],
                treatment_options_points_en=data["treatment_options_points_en"],
                prevention_recommendations_paragraph_ar=data["prevention_recommendations_paragraph_ar"],
                prevention_recommendations_points_ar=data["prevention_recommendations_points_ar"],
                prevention_recommendations_paragraph_en=data["prevention_recommendations_paragraph_en"],
                prevention_recommendations_points_en=data["prevention_recommendations_points_en"],
                status=data["status"]
            )
            return Response({"message":"تم إضافة المرض بنجاح"},status=status.HTTP_201_CREATED)

class DiseaseUpdate(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, pk):
        disease = get_object_or_404(Disease, id=pk)
        data = request.data.copy()
        serializer = DiseaseArabicSerializer(disease, many=False, context={'request': request})
        if not serializer.data:
            return Response({"message": "لا يوجد أي مرض"}, status=status.HTTP_404_NOT_FOUND)
        disease.name_ar = data.get("name_ar", disease.name_ar)
        disease.name_en = data.get("name_en", disease.name_en)
        disease.description_ar = data.get("description_ar", disease.description_ar)
        disease.description_en = data.get("description_en", disease.description_en)
        disease.causes_paragraph_ar = data.get("causes_paragraph_ar", disease.causes_paragraph_ar)
        disease.causes_points_ar = data.get("causes_points_ar", disease.causes_points_ar)
        disease.causes_paragraph_en = data.get("causes_paragraph_en", disease.causes_paragraph_en)
        disease.causes_points_en = data.get("causes_points_en", disease.causes_points_en)
        disease.symptoms_paragraph_ar = data.get("symptoms_paragraph_ar", disease.symptoms_paragraph_ar)
        disease.symptoms_points_ar = data.get("symptoms_points_ar", disease.symptoms_points_ar)
        disease.symptoms_paragraph_en = data.get("symptoms_paragraph_en", disease.symptoms_paragraph_en)
        disease.symptoms_points_en = data.get("symptoms_points_en", disease.symptoms_points_en)
        disease.diagnosis_methods_paragraph_ar = data.get("diagnosis_methods_paragraph_ar", disease.diagnosis_methods_paragraph_ar)
        disease.diagnosis_methods_points_ar = data.get("diagnosis_methods_points_ar", disease.diagnosis_methods_points_ar)
        disease.diagnosis_methods_paragraph_en = data.get("diagnosis_methods_paragraph_en", disease.diagnosis_methods_paragraph_en)
        disease.diagnosis_methods_points_en = data.get("diagnosis_methods_points_en", disease.diagnosis_methods_points_en)
        disease.treatment_options_paragraph_ar = data.get("treatment_options_paragraph_ar", disease.treatment_options_paragraph_ar)
        disease.treatment_options_points_ar = data.get("treatment_options_points_ar", disease.treatment_options_points_ar)
        disease.treatment_options_paragraph_en = data.get("treatment_options_paragraph_en", disease.treatment_options_paragraph_en)
        disease.treatment_options_points_en = data.get("treatment_options_points_en", disease.treatment_options_points_en)
        disease.prevention_recommendations_paragraph_ar = data.get("prevention_recommendations_paragraph_ar", disease.prevention_recommendations_paragraph_ar)
        disease.prevention_recommendations_points_ar = data.get("prevention_recommendations_points_ar", disease.prevention_recommendations_points_ar)
        disease.prevention_recommendations_paragraph_en = data.get("prevention_recommendations_paragraph_en", disease.prevention_recommendations_paragraph_en)
        disease.prevention_recommendations_points_en = data.get("prevention_recommendations_points_en", disease.prevention_recommendations_points_en)
        if data.get("status") == 'true':
            disease.status = True
        else:
            disease.status = False
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
        serializer=DiseaseArabicSerializer(disease,many=False,context={'request': request})
        if not serializer.data:
            return Response({"message":"لم يتم إيجاد المرض"},status=status.HTTP_404_NOT_FOUND)
        else:
            result=disease.delete()
            if result:
                return Response({"message":"تم الحذف بنجاح!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":" لم يتم الحذف "},status=status.HTTP_200_OK)

