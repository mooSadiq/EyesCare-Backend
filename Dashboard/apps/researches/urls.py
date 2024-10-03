from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_view, name='research-view'),
    path('details/<int:id>/', views.research_details_view, name='research-details-view'),
    path('list/', views.ResearchListAPIView.as_view(), name='research-list'),
    path('list/statistics/', views.ResearchStatisticsView.as_view(), name='research-statistics'),
    path('list/<int:pk>/', views.ResearchOneListAPIView.as_view(), name='research-details'),
    path('list/update/<int:pk>/', views.ResearchOneListAPIView.as_view(), name='research-update'),
    path('create/', views.ResearchListAPIView.as_view(), name='research-create'),
    path('journals/page/', views.journals_view, name='journal-view'),
    path('journals/', views.JournalListAPIView.as_view(), name='journal-list'),
    path('journals/create/', views.JournalListAPIView.as_view(), name='journal-create'),
    path('journals/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-one'),
    path('journals/update/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-update'),
    path('journals/delete/<int:pk>/', views.JournalOneListAPIView.as_view(), name='journal-delete'),
    path('fields/page/', views.category_view, name='field-view'),
    path('fields/', views.FieldListAPIView.as_view(), name='field-list'),
    path('fields/create/', views.FieldListAPIView.as_view(), name='field-create'),
    path('fields/<int:pk>/', views.FieldOneListAPIView.as_view(), name='field-one'),
    path('fields/update/<int:pk>/', views.FieldOneListAPIView.as_view(), name='field-update'),
    path('fields/delete/<int:pk>/', views.FieldOneListAPIView.as_view(), name='field-delete'),
]
