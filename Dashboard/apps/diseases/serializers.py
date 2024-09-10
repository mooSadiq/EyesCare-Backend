from rest_framework import serializers
from .models import Disease


class DiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disease
        fields="__all__"