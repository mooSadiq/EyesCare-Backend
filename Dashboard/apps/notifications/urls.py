from django.urls import path
from . import views

urlpatterns = [
    path("get/all/",views.get_notification,name="get_notification"),
    path('read/all/', views.read_all_notifications,name="read_all_notifications"),
    path('read/<int:notification_id>/', views.read_notification,name="read_notification"),
    path('delete/<int:notification_id>/', views.delete_notification,name="delete_notification")
]