from django.urls import path
from . import views 
urlpatterns = [
    #    مسارات التنقل بين الصفحات في الداش بورد
    path('', views.index, name='usersList'),
    path('accountSettings/', views.my_account_settings, name='my_account_settings'),
    path('profile/<int:id>/', views.userProfile, name='user_profile'),
    
    # //////////////////////
    # مسارات API الخاص بالداش بورد
    path('api/get/users/', views.UserListView.as_view(), name='user-list'),
    path('api/get/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('api/delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete-user'),
    path('api/add/', views.CreateUserView.as_view(), name='add-user'),
    path('api/update/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path('api/activation/<int:pk>/', views.UserActivationView.as_view(), name='user-activation'),
    path('api/profile/', views.CuurentUserDetailView.as_view(), name='profile-data'),
    path('api/profile/update/', views.update_myProfile, name='update_myProfile'),
    # //////////////////////
    # مسارات API الخاص  بالتطبيق
    
]
