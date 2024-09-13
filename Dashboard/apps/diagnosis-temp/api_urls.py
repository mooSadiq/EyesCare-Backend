from django.urls import path
from . import mobile_api

urlpatterns = [
    path('', mobile_api.ImageInferenceView.as_view(), name='diagnosis-infer'),
]
