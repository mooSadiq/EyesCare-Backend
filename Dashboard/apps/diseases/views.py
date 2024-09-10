from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .models import Disease
from .serializers import DiseasesSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

def diseases_list(request):
    return render(request, 'diseases_list.html')

def diseases_details(request):
    return render(request, 'diseases_details.html')

def edit_diseases_details(request):
    return render(request, 'edit-diseases-details.html')

#Return All Diseases From DB
@api_view(['GET'])
def get_all_diseases(request):
    diseases=Disease.objects.all()
    serializer=DiseasesSerializer(diseases,many=True)
    if serializer.data:
        return Response({"Diseases":serializer.data},status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status.HTTP_404_NOT_FOUND)

#Return one Disease From DB by id
@api_view(['GET'])
def get_disease_by_id(request,pk):
    disease=get_object_or_404(Disease,id=pk)
    serializer=DiseasesSerializer(disease,many=False)
    if serializer.data:
        return Response({"Diseases":serializer.data},status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status.HTTP_404_NOT_FOUND)

#جلب مرض عن طريق الأسم
@api_view(['GET'])
def get_all_diseases_byname(request,nameresartch):
    nameresartch = nameresartch.strip()
    disease=Disease.objects.filter(name=nameresartch)
    serializer=DiseasesSerializer(disease,many=False)
    if serializer.data:
        return Response({"Diseases":serializer.data},status.HTTP_200_OK)
    else :
        return Response({"Info":"There is not any deases"},status.HTTP_404_NOT_FOUND)

@api_view(['img-fluid'])
def set_diseas(request):
    disease=Disease.objects.filter(name=request.data['name'])
    if disease.exists():
        return Response({"Info":"This Diseas is already exists"})
    else:
        data=request.data
        print(data)
        Disease.objects.create(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            causes=data["causes"],
            symptoms=data["symptoms"],
            diagnosis_methods=data["diagnosis_methods"],
            treatment_options=data["treatment_options"],
            prevention_recommendations=data["prevention_recommendations"]
        )
        return Response({"message":"تم إضافة المرض بنجاح"},status.HTTP_201_CREATED)

@api_view(['PUT'])
def upadate_disease(request,pk):
    disease=get_object_or_404(Disease,id=pk)
    serializer=DiseasesSerializer(disease,many=False)
    if not serializer.data:
        return Response({"message":"لايوجد اي مرض"},status.HTTP_404_NOT_FOUND)
    else:
        disease.name=request.data["name"]
        disease.description=request.data["description"]
        disease.image=request.data["image"]
        disease.causes=request.data["causes"]
        disease.symptoms=request.data["symptoms"]
        disease.diagnosis_methods=request.data["diagnosis_methods"]
        disease.treatment_options=request.data["treatment_options"]
        disease.prevention_recommendations=request.data["prevention_recommendations"]
        disease.save()
        return Response({"message":"تم تحديث المرض بنجاح"},status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_diseases(request,pk):
    disease=get_object_or_404(Disease,id=pk)
    serializer=DiseasesSerializer(disease,many=False)
    if not serializer.data:
        return Response({"message":"لم يتم إيجاد المرض"},status.HTTP_404_NOT_FOUND)
    else:
        result=disease.delete()
        if result:
            return Response({"message":"تم الحذف بنجاح!"},status.HTTP_200_OK)
        else:
            return Response({"message":" لم يتم الحذف "},status.HTTP_200_OK)

