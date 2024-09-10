from django.db.models import Q
import django_filters as filters
from .models import Post

class PostFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search')
    year = filters.NumberFilter(field_name='created_at', lookup_expr='year')
    month = filters.NumberFilter(field_name='created_at', lookup_expr='month')
    image = filters.ChoiceFilter(choices=[
        ('with-image', 'With Image'),
        ('without-image', 'Without Image')
    ], method='filter_by_image')
    date_order = filters.OrderingFilter(fields=[('created_at', 'created_at')])
    interaction_order = filters.OrderingFilter(fields=[('likes_count', 'likes_count')])
    views_order = filters.OrderingFilter(fields=[('views_count', 'views_count')])

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(text__icontains=value)
        )

    def filter_by_image(self, queryset, name, value):
        if value == 'with-image':
            return queryset.filter(image__isnull=False)
        elif value == 'without-image':
            return queryset.filter(image__isnull=True)
        return queryset

    class Meta:
        model = Post
        fields = ['search', 'year', 'month', 'image', 'date_order', 'interaction_order', 'views_order']
