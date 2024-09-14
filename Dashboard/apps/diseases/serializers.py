from rest_framework import serializers
from .models import Disease
from urllib.parse import urljoin

class DiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disease
        fields="__all__"
        
class DiseaseArabicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_ar')
    description = serializers.CharField(source='description_ar')
    causes = serializers.JSONField(source='causes_ar')
    symptoms = serializers.JSONField(source='symptoms_ar')
    diagnosis_methods = serializers.JSONField(source='diagnosis_methods_ar')
    treatment_options = serializers.JSONField(source='treatment_options_ar')
    prevention_recommendations = serializers.JSONField(source='prevention_recommendations_ar')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'name_en', 'description', 'image', 'causes', 
            'symptoms', 'diagnosis_methods', 'treatment_options', 'prevention_recommendations'
        ]
        
    def get_image(self, obj):
        if hasattr(obj, 'image') and obj.image:
            domain = self.context.get('request').get_host()
            return urljoin(f'http://{domain}', obj.image.url)
        return None
                
class DiseaseEnglishSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_en')
    description = serializers.CharField(source='description_en')
    causes = serializers.JSONField(source='causes_en')
    symptoms = serializers.JSONField(source='symptoms_en')
    diagnosis_methods = serializers.JSONField(source='diagnosis_methods_en')
    treatment_options = serializers.JSONField(source='treatment_options_en')
    prevention_recommendations = serializers.JSONField(source='prevention_recommendations_en')
    image = serializers.SerializerMethodField()

    
    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'description', 'image', 'causes', 
            'symptoms', 'diagnosis_methods', 'treatment_options', 'prevention_recommendations'
        ]
        
    def get_image(self, obj):
        if hasattr(obj, 'image') and obj.image:
            domain = self.context.get('request').get_host()
            return urljoin(f'http://{domain}', obj.image.url)
        return None