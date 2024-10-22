from rest_framework import serializers
from apps.doctor.models import Doctor
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    doctor_id = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'first_name',  
            'last_name',   
            'gender', 
            'birth_date', 
            'user_address',
            'profile_picture', 
            'phone_number', 
            'email',
            'user_type',
            'is_blue_verified',
            'is_active',
            'auth_provider',
            'user_address',
            'doctor_id', 
            'patient_id' 
        ] 
    def get_doctor_id(self, obj):
        return obj.doctor.id if hasattr(obj, 'doctor') else None
    def get_patient_id(self, obj):
        return obj.patient.id if hasattr(obj, 'patient') else None
    def get_user_address(self, obj):
        return obj.user_address.governorate if hasattr(obj, 'user_address') and obj.user_address.governorate else None

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class DoctorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    gender = serializers.CharField(source='user.gender') 
    birth_date = serializers.DateField(source='user.birth_date')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    phone_number = serializers.IntegerField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    user_address = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id', 
            'first_name',  
            'last_name',   
            'gender', 
            'birth_date', 
            'user_address',
            'profile_picture', 
            'phone_number', 
            'email',
            'specialization', 
            'hospital', 
            'address', 
            'about', 
            'start_time_work', 
            'end_time_work'
        ]    
    def get_user_address(self, obj):
        user_address = getattr(obj.user, 'user_address', None)
        return user_address.governorate if user_address and user_address.governorate else None


  
class UserProfileSerializer(serializers.ModelSerializer):
    user_address = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'gender', 'birth_date', 'profile_picture',
                  'phone_number' ,'user_address']
        
    def get_user_address(self, obj):
        return obj.user_address.governorate if hasattr(obj, 'user_address') and obj.user_address.governorate else None

class DoctorUpdateProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Doctor
        fields = [
            'specialization', 
            'hospital', 
            'address', 
            'about', 
            'start_time_work', 
            'end_time_work',
            'user',
        ]    
