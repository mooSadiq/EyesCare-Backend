from rest_framework import serializers
from .models import Research, Journal, Field
from apps.users.models import CustomUser
from datetime import datetime
from urllib.parse import urljoin

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = "__all__"
        
        
class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"
