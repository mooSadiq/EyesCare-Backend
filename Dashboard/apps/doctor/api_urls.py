from django.urls import path
from . import mobile_api

urlpatterns=[
    path('getDoctorData/', mobile_api.DoctorView.as_view(), name="get_data"),
    path('getAllDoctors/', mobile_api.DoctorsListView.as_view(), name="get_doctors"),
]