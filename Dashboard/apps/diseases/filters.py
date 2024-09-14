from django.db.models import Q
from django.db.models.expressions import RawSQL
import django_filters as filters
from .models import Disease

class DiseaseFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search')

    def filter_by_search(self, queryset, name, value):
            return queryset.filter(
                Q(name_ar__icontains=value) |
                Q(name_en__icontains=value) |
                Q(description_ar__icontains=value) |
                Q(description_en__icontains=value) 
                # Q(RawSQL("JSON_UNQUOTE(causes_ar->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(causes_ar->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(causes_en->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(causes_en->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(symptoms_ar->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(symptoms_ar->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(symptoms_en->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(symptoms_en->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(diagnosis_methods_ar->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(diagnosis_methods_ar->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(diagnosis_methods_en->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(diagnosis_methods_en->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(treatment_options_ar->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(treatment_options_ar->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(treatment_options_en->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(treatment_options_en->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(prevention_recommendations_ar->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(prevention_recommendations_ar->'$.points', %s, '$')", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(prevention_recommendations_en->'$.paragraph') LIKE %s", [f'%{value}%'])) |
                # Q(RawSQL("JSON_UNQUOTE(prevention_recommendations_en->'$.points', %s, '$')", [f'%{value}%'])) 

            )

    class Meta:
        model = Disease
        fields = ['search']
