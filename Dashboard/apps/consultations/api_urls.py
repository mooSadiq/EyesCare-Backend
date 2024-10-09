from django.urls import path
from . import mobile_api

urlpatterns = [
    path('send/', mobile_api.ConsultationSendAPIView.as_view(), name='consultations-send'),
]

