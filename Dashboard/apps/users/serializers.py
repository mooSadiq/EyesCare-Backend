from rest_framework import serializers
from apps.doctor.models import Doctor
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class DoctorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    gender = serializers.CharField(source='user.gender')  # تأكد من وجود هذا الحقل في User model
    birth_date = serializers.DateField(source='user.birth_date')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    phone_number = serializers.CharField(source='user.phone_number')  # الأفضل تحويله إلى CharField
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Doctor
        fields = [
            'id', 
            'first_name',  
            'last_name',   
            'gender', 
            'birth_date', 
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


  
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'gender', 'birth_date', 'profile_picture',
                  'phone_number' ]
        


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
