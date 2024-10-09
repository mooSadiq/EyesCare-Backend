from django.urls import path
from . import mobile_api
from . import google_auth

urlpatterns = [
    path('register/', mobile_api.RegisterUserView.as_view(), name='register'),
    path('verifyemail/', mobile_api.VerifyEmailApiCodeView.as_view(), name='verify-email-code'),
    path('login/', mobile_api.LoginView.as_view()),
    path('login/google/', google_auth.GoogleLoginView.as_view()),
    path('password/forgot/', mobile_api.ForgotPasswordView.as_view(), name='password-forgot'),
    path('password/verifycode/', mobile_api.VerifyApiCodeView.as_view(), name='password-verify-code'),
    path('password/reset/', mobile_api.SetNewPasswordView.as_view(), name='set-new-password'),
]