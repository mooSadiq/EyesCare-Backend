from django.urls import path
from . import views

urlpatterns = [
    # Dashboard urls
    path('', views.doctors_list, name='doctorssList'),
    path('profile/<int:id>/', views.doctorProfile, name='doctor-profile'),
    
    #/////////////////
    # مسارات API الخاص بالداش بورد
    path('api/getDoctors/', views.get_all_doctors),
    path('api/getDoctors/<int:pk>/', views.DoctorDetailView.as_view(),name='get_by_id_doctor'),
    path('api/delete/Doctors/<int:pk>/', views.DeleteDoctorView.as_view(),name='delete_doctor'),
    path('api/add_Doctors/', views.AddDoctorView.as_view(), name='add_doctor'),
    path('api/profile/update/<int:id>/', views.update_doctor, name='update_doctor'),
    
    #/////////////////////
    # مسارات API الخاص  بالتطبيق
]


