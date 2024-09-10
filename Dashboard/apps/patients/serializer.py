from rest_framework import serializers
from apps.users.models import CustomUser
from .models import Patient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'gender', 'birth_date', 'profile_picture',
                  'phone_number', 'user_type','is_active', 'is_verified',
                  'date_joined', 'is_blue_verified'
                  ]

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'subscription_count', 'subscription_status']

