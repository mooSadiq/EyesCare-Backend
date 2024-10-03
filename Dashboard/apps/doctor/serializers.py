from rest_framework import serializers
from apps.users.models import CustomUser
from .models import Doctor, City

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

class DoctorListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)


    class Meta:
        model = Doctor
        fields = ['id', 'name', 'profile_picture', 'address']

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class DoctorOneSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    phone = serializers.IntegerField(source='user.phone_number', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'profile_picture', 'specialization', 'hospital', 'address', 'about', 'start_time_work', 'end_time_work', 'phone', 'email']
       
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']
