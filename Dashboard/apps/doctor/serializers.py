from rest_framework import serializers
from apps.users.models import CustomUser
from .models import Doctor

# Reuse the UserSerializer for the user field in Doctor
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture', 
                  'gender', 'birth_date', 'phone_number', 'user_type', 
                  'is_verified', 'is_active', 'is_blue_verified']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = "__all__"

class AddDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
