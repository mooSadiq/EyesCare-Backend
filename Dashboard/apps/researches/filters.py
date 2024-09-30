from django.db.models import Q
import django_filters as filters
from .models import Journal, Field, Research

class ResearchFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search')
    journal = filters.ModelChoiceFilter(queryset=Journal.objects.all(), required=False)
    field = filters.ModelChoiceFilter(queryset=Field.objects.all(), required=False)
    
    publication_date_from = filters.DateFilter(field_name='publication_date', lookup_expr='gte', label='From Date')
    publication_date_to = filters.DateFilter(field_name='publication_date', lookup_expr='lte', label='To Date')
    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(abstract__icontains=value) |
            Q(institution__icontains=value) |
            Q(authors__icontains=value)
        )
        
    class Meta:
        model = Research
        fields = ['journal', 'field', 'publication_date_from', 'publication_date_to']
