"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Dashboard urls
    path("", include("apps.home.urls")),
    # users
    path("users/", include("apps.users.urls")),
    path("api/profile/", include("apps.users.api_urls")),
    
    # patients
    path("patients/", include("apps.patients.urls")),
    path('api/patients/', include("apps.patients.api_urls")),

    # doctor
    path("doctors/", include("apps.doctor.urls")),
    path("api/doctors/", include("apps.doctor.api_urls")),
    # emails
    path("emails/", include("apps.emails.urls")),
    # doctors not important
    path("doc/", include("doctors.urls")),

    path('patients/', include("apps.patients.urls")),
    # posts
    path('posts/', include("apps.posts.urls")),
    path('api/posts/', include("apps.posts.api_urls")),
    # doctors
    path('doc/', include("doctors.urls")),
    # diagnosis history
    path('diagnosis/', include("apps.diagnosis.urls")),
    path('api/diagnosis/', include("apps.diagnosis.api_urls")),
    # advertisements 
    path('advertisements/', include("apps.advertisements.urls")),
    path('api/advertisements/', include("apps.advertisements.api_urls")),
    # authentication
    path('auth/', include("authentication.urls")),
    path('api/auth/', include("authentication.api_urls")),
    # diseases
    path('diseases/', include("apps.diseases.urls")),
    path('api/diseases/', include("apps.diseases.api_urls")),
    # evaluations
    path('evaluations/', include("apps.evaluations.urls")),
    path('api/evaluations/', include("apps.evaluations.api_urls")),
    
    path('api/token/',  TokenObtainPairView.as_view()),
    #chat
    path('chat/', include('apps.chat.urls')),
    path('api/chat/', include('apps.chat.api_urls')),
    
    #consultations
    path('consultations/', include('apps.consultations.urls')),
    path('api/consultations/', include('apps.consultations.api_urls')),
    
    
    #notifications
    path('notifications/', include('apps.notifications.urls')),
    #Research
    path('researches/', include('apps.researches.urls')),
    path('api/researches/', include('apps.researches.api_urls')),
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
