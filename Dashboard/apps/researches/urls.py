from django.urls import path
from . import views

urlpatterns = [
    path('researches/', views.ResearchListAPIView.as_view(), name='research-list'),
    path('researches/create/', views.ResearchCreatetAPIView.as_view(), name='research-create'),
]
