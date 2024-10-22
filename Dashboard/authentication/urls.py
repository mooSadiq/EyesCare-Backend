from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login",),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("forgot_password/", views.ForgetPasswordView.as_view(), name="forgot-password",),
    path("verification_code/", views.VerifytCodeView.as_view(), name="verification-coding",),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset-password",),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/login/page/', views.googlepage, name='google-page'),

]

