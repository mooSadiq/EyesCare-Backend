from django.urls import path
from . import mobile_api 
urlpatterns = [
    path('', mobile_api.CuurentUserDetailView.as_view(), name='profile-data'),
]
