from rest_framework import serializers
from apps.users.models import CustomUser
from .models import Patient, SubscriptionPlan, PatientSubscription

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

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSubscription
        fields = ['patient', 'plan', 'start_date', 'end_date', 'is_active', 'remaining_consultations']

