from django.db.models import Q
import django_filters as filters
from .models import Journal, Field, Research

class ResearchFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search')
    journal = filters.ModelChoiceFilter(queryset=Journal.objects.all(), required=False)
    field = filters.ModelChoiceFilter(queryset=Field.objects.all(), required=False)
      
    publication_date_from = filters.NumberFilter(field_name='publication_date', lookup_expr='year__gte', label='Year From')
    publication_date_to = filters.NumberFilter(field_name='publication_date', lookup_expr='year__lte', label='Year To')
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
