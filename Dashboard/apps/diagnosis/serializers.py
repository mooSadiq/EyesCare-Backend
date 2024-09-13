from rest_framework import serializers
from apps.diseases.models import Disease
from apps.patients.models import Patient
from apps.users.models import CustomUser
from .models import DiagnosisReport

# Reuse the UserSerializer for the user field in Doctor
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture', 
                  'gender', 'birth_date', 'phone_number', 'user_type', 
                  'is_verified', 'is_active', 'is_blue_verified']  # أضف الحقول التي تريد عرضها من نموذج User

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # تضمين بيانات المستخدم

    class Meta:
        model = Patient
        fields = "__all__" #['id', 'user']  # أضف أو احذف الحقول حسب الحاجة

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"  #['id', 'name', 'description']  # أضف أو احذف الحقول حسب الحاجة

class DiagnosisSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    disease = DiseaseSerializer()

    class Meta:
        model = DiagnosisReport
        fields = "__all__"  #['id', 'patient', 'disease', 'diagnosis_date']  # أضف أو احذف الحقول حسب الحاجة
        
        


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
