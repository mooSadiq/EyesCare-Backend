from django.urls import path
from . import views
urlpatterns = [
    path('', views.chatview, name="chat_list"),
    ]
