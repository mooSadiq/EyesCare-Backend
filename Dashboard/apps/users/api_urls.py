from django.urls import path
from . import mobile_api 
urlpatterns = [
    path('', mobile_api.CuurentUserDetailView.as_view(), name='profile-data'),
    path('update/', mobile_api.UpdateProfileView.as_view(), name='profile-update'),
    path('change/password/', mobile_api.ChangePasswordView.as_view(), name='change-password'),
    path('cities/', mobile_api.GovernoratesListAPIView.as_view(), name="cities-list"),
    path('address/', mobile_api.CreateUserAddressAPIView.as_view(), name="address-create"),
]
