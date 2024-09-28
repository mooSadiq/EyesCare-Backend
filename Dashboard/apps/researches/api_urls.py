from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResearchListAPIView.as_view(), name='research-list'),
    path('filters/', views.ResearchFilterListAPIView.as_view(), name='research-filters'),
    path('<int:pk>/', views.ResearchAPIView.as_view(), name='research-one'),
    path('journals/', views.JournalListAPIView.as_view(), name='journal-list'),
    path('fields/', views.FieldListAPIView.as_view(), name='field-list'),
]
