from django.urls import path
from . import api_mobile

urlpatterns = [
    path('get/',api_mobile.AdvertisementList.as_view(),name="get_mobile_advertisements"),
    path('clicks/<int:pk>/',api_mobile.AddClick.as_view(),name="add_click"),
    path('views/<int:pk>/',api_mobile.AddViews.as_view(),name="add_views")
]