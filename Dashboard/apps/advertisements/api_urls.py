from django.urls import path
from . import api_mobile

urlpatterns = [
    path('',api_mobile.AdvertisementList.as_view(),name="get_mobile_advertisements"),
    path('click/<int:pk>/',api_mobile.AddClick.as_view(),name="add_click"),
    path('views/',api_mobile.AddViews.as_view(),name="add_views")
]