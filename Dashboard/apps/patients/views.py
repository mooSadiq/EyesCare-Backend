from django.shortcuts import get_object_or_404, redirect, render
from .models import Patient
from rest_framework.views import APIView
from apps.users.models import CustomUser
from .serializers import PatientSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
# Create your views here.

# دوال العرض والانتقال بين الصفحات في الداش بورد
def index(request):
  return render(request, 'patients_list.html')
def patientProfile(request,id):  
    return render(request, 'patient_profile.html', {"patient_id": id})
  

class PatientListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.all()
        patients_serializer = PatientSerializer(patients, many=True)
        users = CustomUser.objects.all()
        users_serializer = UserSerializer(users, many=True)  
        return Response({'patients': patients_serializer.data,
                          'users':users_serializer.data,}, status=status.HTTP_200_OK)
      
class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        patient = Patient.objects.filter(id=pk).first()        
        if patient is None:
            return Response({"message": "المريض غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
      
class DeletePatientView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        patient = get_object_or_404(Patient, id=pk)
        user_id = patient.user.id
        
        delete_result = patient.delete()
        if delete_result[0] > 0:
            user = CustomUser.objects.get(id=user_id)
            user.user_type = 'user'
            user.save()
            return Response({"message": "تم الحذف بنجاح!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "لم يتم الحذف "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
    
    
class AddPatientView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.data.get('user_id')
        user = CustomUser.objects.filter(id=user_id).first()
        
        if not user:
            return Response({"message": "لم يتم العثور على المستخدم"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(user, 'patient'):
            return Response({"message": "هذا المستخدم موجود في جدول الامراض"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.user_type = 'patient'
        user.save()
        
        Patient.objects.create(user=user)
        return Response({"message": "تم اضافة بيانات المريض بنجاح"}, status=status.HTTP_201_CREATED)


