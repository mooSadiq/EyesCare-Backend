from django.urls import path
from . import views

urlpatterns = [
    path("get/all/",views.get_notification,name="get_notification"),
]