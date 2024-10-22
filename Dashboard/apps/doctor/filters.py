from django.db.models import Q
import django_filters as filters
from .models import Doctor

class DoctorFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search')
    city = filters.CharFilter(method='filter_by_city')
      
    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(specialization__icontains=value) |
            Q(hospital__icontains=value)
        )
    def filter_by_city(self, queryset, name, value):
        return queryset.filter(
            Q(address__icontains=value)
        )
        
    class Meta:
        model = Doctor
        fields = ['search', 'city']
