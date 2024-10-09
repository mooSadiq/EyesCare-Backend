from django.urls import path
from . import mobile_api

urlpatterns = [
    path('', mobile_api.ResearchFilterListAPIView.as_view(), name='research-list'),
    path('filters/', mobile_api.ResearchFilterListAPIView.as_view(), name='research-filters'),
    path('<int:pk>/', mobile_api.ResearchOneListAPIView.as_view(), name='research-one'),
    path('journals/', mobile_api.JournalListAPIView.as_view(), name='journal-list'),
    path('fields/', mobile_api.FieldListAPIView.as_view(), name='field-list'),
]
