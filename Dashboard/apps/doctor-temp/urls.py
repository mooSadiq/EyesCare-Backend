from django.urls import path
from . import views

urlpatterns = [
    # Dashboard urls
    path('', views.doctors_list, name='doctorssList'),
    path('profile', views.userProfile, name='doctor-profile')
]

