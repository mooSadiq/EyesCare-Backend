from rest_framework import serializers

from apps.patients.models import Patient
from apps.doctor.models import Doctor
from apps.users.models import CustomUser
from .models import Consultation

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture']

class DoctorSerializer(serializers.ModelSerializer):
    # استبدل `user` هنا بـ `UserMinimalSerializer` لعرض الحقول المطلوبة
    class Meta:
        model = Doctor
        fields = ['id', 'UserMinimalSerializer', 'address', 'hospital', 'specialization', 'about']

class PatientSerializer(serializers.ModelSerializer):
    # استبدل `user` هنا بـ `UserMinimalSerializer` لعرض الحقول المطلوبة
    class Meta:
        model = Patient
        fields = ['id', 'UserMinimalSerializer', 'subscription_count', 'subscription_status']

class ConsultationSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    
    class Meta:
        model = Consultation
        fields = ['id', 'is_complete', 'consultation_date', 'patient', 'doctor']

    def get_patient(self, obj):
        # جلب المستخدم من خلال نموذج Patient
        user = obj.patient.user
        return {
            'id': obj.patient.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture.url,
        }

    def get_doctor(self, obj):
        # جلب المستخدم من خلال نموذج Doctor
        user = obj.doctor.user
        return {
            'id': obj.doctor.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture.url,
        }

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture']
        
# class DoctorSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = Doctor
#         fields = "__all__"
        
# class PatientSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Patient
#         fields = ['id', 'user', 'subscription_count', 'subscription_status']


# class ConsultationSerializer(serializers.ModelSerializer):
#     patient = PatientSerializer()
#     doctor = DoctorSerializer()
#     class Meta:
#         model = Consultation
#         fields = ['id', 'patient', 'doctor', 'is_complete', 'consultation_date']
        
        