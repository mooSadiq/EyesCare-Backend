from django.urls import path
from . import mobile_api

urlpatterns=[
    path('getDoctorData/', mobile_api.DoctorView.as_view(), name="get_data"),
    path('', mobile_api.DoctorFilterListAPIView.as_view(), name="doctors-list"),
    path('<int:pk>/', mobile_api.DoctorOneListAPIView.as_view(), name="doctor-details"),
    path('cities/', mobile_api.CityListAPIView.as_view(), name="cities-list"),
    path('filter/', mobile_api.DoctorFilterListAPIView.as_view(), name="doctors-filter-list"),
]