from django.urls import path
from . import views 

urlpatterns = [
    path('api/getConsultation/', views.index , name='consultation_list'),
    path('api/getConsultations/', views.ConsultationListView.as_view(), name='consultation_listt'),
    path('api/delete/<int:pk>/', views.ConsultationDetailView.as_view(), name='consultation_delete'),
]
