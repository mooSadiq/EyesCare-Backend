from django.urls import path
from . import views

urlpatterns = [
    #  مسارات التنقل بين الصفحات في الداش بورد
    path('', views.index, name='patientsList'),
    path('profile/<int:id>/', views.patientProfile, name='patient_profile'),
    
    #/////////////////
    # مسارات API الخاص بالداش بورد
    path('api/get/patients/', views.PatientListView.as_view(), name='patient-list'),
    path('api/get/patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('api/delete/<int:pk>/', views.DeletePatientView.as_view(), name='delete-patient'),
    path('api/add/', views.AddPatientView.as_view(), name='add-patient'),
    
    #/////////////////////

]
