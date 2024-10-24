
from rest_framework import serializers
from .models import Advertisement

# Reuse the UserSerializer for the user field in Doctor


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = "__all__"
        
        

class AdvertisementSerializerMobile(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ["id","advertiser","phone_number","ad_link","ad_image","about"]