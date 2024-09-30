
from django.urls import path
from . import api_mobile

urlpatterns = [
    path('get/reviews/',api_mobile.get_all_reviews,name='get_all_reviews'),
    path('delete/<int:pk>/',api_mobile.delete_review,name='delete_review'),
    path('update/<int:pk>/',api_mobile.update_review,name='update_review'),
    path('set/',api_mobile.set_review,name='set_review'),
]