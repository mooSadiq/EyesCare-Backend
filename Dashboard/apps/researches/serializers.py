from rest_framework import serializers
from .models import Research, Journal, Field
from apps.users.models import CustomUser
from datetime import datetime
from urllib.parse import urljoin
from django.utils.timesince import timesince

class ResearchSerializer(serializers.ModelSerializer):
    journal_abbreviation = serializers.CharField(source='journal.abbreviation', read_only=True)
    field_name = serializers.CharField(source='field.name', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title', 'abstract', 'publication_date', 'journal_abbreviation', 'journal', 'field_name', 'is_file']

class ResearchListSerializer(serializers.ModelSerializer):
    journal_abbreviation = serializers.CharField(source='journal.abbreviation', read_only=True)
    journal = serializers.CharField(source='journal.name', read_only=True)
    field_name = serializers.CharField(source='field.name', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title', 'abstract', 'publication_date', 'journal_abbreviation', 'journal', 'field_name', 'authors', 'institution', 'file', 'is_file', 'url', 'downloads_count']
    
class ResearchOneSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    journal_name = serializers.CharField(source='journal.name', read_only=True)
    journal_id = serializers.CharField(source='journal.id', read_only=True)
    field_name = serializers.CharField(source='field.name', read_only=True)
    field_id = serializers.IntegerField(source='field.id', read_only=True)
    class Meta:
        model = Research
        fields = ['id', 'title', 'abstract', 'publication_date', 'journal_name', 'journal_id', 'field_id', 'field_name', 'authors', 'institution', 'file', 'is_file', 'url', 'downloads_count', 'views_count', 'user_name', 'profile_picture']
       
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def get_profile_picture(self, obj):
        domain = self.context.get('request').get_host()
        if obj.user.profile_picture:
            return urljoin(f'http://{domain}',obj.user.profile_picture.url)
        return None
        
class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"
class ResearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = "__all__"
        read_only_fields = ['user']


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"



class StatisticsSerializer(serializers.Serializer):
    research_count = serializers.IntegerField()
    field_count = serializers.IntegerField()
    journal_count = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    pdf_count = serializers.IntegerField()
    no_pdf_count = serializers.IntegerField()
