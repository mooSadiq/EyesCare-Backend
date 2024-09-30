from rest_framework import serializers
from .models import Research, Journal, Field
from apps.users.models import CustomUser
from datetime import datetime
from urllib.parse import urljoin

class ResearchSerializer(serializers.ModelSerializer):
    journal_abbreviation = serializers.CharField(source='journal.abbreviation', read_only=True)
    field_name = serializers.CharField(source='field.name', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title', 'abstract', 'publication_date', 'journal_abbreviation', 'field_name', 'authors', 'institution', 'file', 'downloads_count']
    
class ResearchOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ['file']
   
        
class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"
