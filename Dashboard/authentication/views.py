import random
from config import settings
from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PasswordResetSerializer
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views import View
from django.contrib import messages
from apps.users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def generate_verification_code():
    return random.randint(100000, 999999)

def send_verification_email(email, verification_code):
    subject = 'رمز التحقق الخاص بك'
    message = f'رمز التحقق الخاص بك هو: {verification_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]    
    
    num_sent = send_mail(subject, message, email_from, recipient_list)
    return num_sent > 0  


class LoginView(TemplateView):
    template_name = "auth/login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return super().get(request)

    def post(self, request):
        if request.method != 'POST':
            return JsonResponse({'message': 'يجب استخدام  POST فقط.'}, status=405)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'بيانات غير صالحة.'}, status=400)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({'message': 'يرجى إدخال البريد الإلكتروني وكلمة المرور.'}, status=400)

        user = CustomUser.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return JsonResponse({'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'}, status=401)
        if user.user_type != 'admin':
            return JsonResponse({'message': 'عذرا ليس لديك حق الوصول.'}, status=401)

        try:
            login(request, user)
        except Exception as e:
            return JsonResponse({'message': 'حدث خطأ أثناء تسجيل الدخول.'}, status=500)

        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
        except Exception as e:
            return JsonResponse({'message': 'خطأ أثناء إنشاء التوكنات.'}, status=500)

        next_url = request.POST.get("next") or request.GET.get("next") or "/"
        domain = request.get_host()
        profile_picture =  f"http://{domain}{user.profile_picture.url}"
        user_data = {
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_type': user.user_type,
            'profile_picture': profile_picture if profile_picture else None, 
        }

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'next_url': next_url,
            'user': user_data
        }

        return JsonResponse({
                        'status': status.HTTP_200_OK,
                        'message': "تم تسجيل الدخول بنجاح",
                        'data': response_data,
                        }, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        logout(request)  
        refresh_token = request.data.get("refresh", None)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                pass  
        
        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم تسجيل الخروج بنجاح'
        }, status=status.HTTP_200_OK)
        
    
                
class ForgetPasswordView(TemplateView):
    template_name = "auth/forgot_password.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index") 

        return super().get(request)
    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("email")

            user = CustomUser.objects.filter(email=email).first()
            if not user:
                messages.error(request, "No user with this email exists.")
                return redirect("forgot-password")

            verification_code = generate_verification_code()            
            expiration_time = timezone.now() + timedelta(minutes=3)
            user.verification_code = verification_code
            user.verification_code_expiry = expiration_time
            user.save()

            if send_verification_email(email, verification_code):
                request.session['email'] = email  
                return redirect('verification-coding')
            else:
                messages.error(request, "Email settings are not configured. Unable to send verification email.")
                return redirect("forgot-password")
        return redirect("forgot-password")  
              
class VerifytCodeView(TemplateView):
    template_name = "auth/verify_code.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")  
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            verify_code = request.POST.get("verification_code")
            email = request.session.get('email')
            user = CustomUser.objects.filter(
                email=email,
                verification_code=verify_code,
                verification_code_expiry__gt=timezone.now()
            ).first()            
            if not user:
                messages.error(request, 'الكود خطا او انتهت صلاحيته')
                return redirect("verification-coding")
            return redirect('reset-password')
              
        return redirect('verification-coding')

class ResetPasswordView(TemplateView):
    template_name= "auth/reset_password.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index") 
        return super().get(request)

    def post(self, request):
          if request.method == "POST":
              new_password = request.POST.get("password")
              email = request.session.get('email')
              user = CustomUser.objects.filter(
                  email=email,
                  verification_code_expiry__gt=timezone.now()
              ).first()
              if user:
                  extended_expiry_time = user.verification_code_expiry + timedelta(minutes=5)
                  if extended_expiry_time < timezone.now():
                      messages.error(request, "انتهت صلاحية الكود")
                      return redirect("forgot-password")
                
                  user.set_password(new_password)
                  user.verification_code = None 
                  user.verification_code_expiry = None
                  user.save()
                  request.session['email'] = None
                  return redirect('login')
              messages.error(request, " خطا! المستحدم غير موجود ")
              return redirect("forgot-password")
          return redirect("reset-password")

def forgotPassword(request):
  return render(request, "forgot_password.html")

def send_code_by_email(request):  
  return render(request, "email_message.html")



          
def googlepage(request):
  return render(request, "auth/trygoogle.html")