from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_view, name='research-view'),
    path('list/', views.ResearchListAPIView.as_view(), name='research-'),
    path('create/', views.ResearchCreatetAPIView.as_view(), name='research-create'),
    path('journals/page/', views.journals_view, name='journal-view'),
    path('journals/', views.JournalListAPIView.as_view(), name='journal-list'),
    path('journals/create/', views.JournalListAPIView.as_view(), name='journal-create'),
    path('journals/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-one'),
    path('journals/update/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-one'),
    path('journals/delete/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-one'),
    path('fields/page/', views.category_view, name='field-view'),
    path('fields/', views.FieldListAPIView.as_view(), name='field-list'),
    path('fields/create/', views.FieldCreateAPIView.as_view(), name='field-create'),
    path('fields/<int:pk>/', views.FieldOneListAPIView.as_view(), name='field-one'),
]
