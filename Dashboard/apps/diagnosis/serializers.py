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
    diagnosis_status = serializers.CharField(source='diagnosis_result', read_only=True)
    image_path = serializers.ImageField(source='image')
    confidence = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=2)
    diagnosis_date = serializers.DateField()
    compeleted = serializers.BooleanField()

    class Meta:
        model = DiagnosisReport
        fields = ['diagnosis_status', 'diagnosis_date', 'image_path', 'confidence', 'compeleted']

class DiagnosisSerializerDash(serializers.ModelSerializer):
    patient=PatientSerializer()
    disease=DiseaseSerializer()
    class Meta:
        model = DiagnosisReport
        fields ='__all__'


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
