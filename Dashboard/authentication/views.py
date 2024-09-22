import random
from django.conf import settings
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
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
# Create your views here.

# دالة توليد كود عشوائي
def generate_verification_code():
    # توليد رقم عشوائي من ست خانات.
    return random.randint(100000, 999999)

# دالة ارسال الكود
def send_verification_email(email, verification_code):
    subject = 'رمز التحقق الخاص بك'
    message = f'رمز التحقق الخاص بك هو: {verification_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]    
    
    num_sent = send_mail(subject, message, email_from, recipient_list)
    return num_sent > 0  # تحقق من نجاح الإرسال


class LoginView(TemplateView):
    template_name = "auth/login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return super().get(request)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse({'message': 'يرجى إدخال البريد الإلكتروني وكلمة المرور.'}, status=400)
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return JsonResponse({'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'}, status=400)

        # تسجيل الدخول
        login(request, user)

        # إنشاء توكنات JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # إعداد URL الصفحة التالية
        next_url = request.POST.get("next") or request.GET.get("next") or "/"

        # إرسال التوكنات والـ URL كاستجابة JSON
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'next_url': next_url,
        }
        return JsonResponse(response_data)
      
class LogoutView(View):
    def post(self, request):
        logout(request)
        refresh_token = request.headers.get('refreshToken')
        if refresh_token:
            try:
                # إزالة التوكن من خلال إعداد التوكن على أنه غير صالح
                token = refresh_token.split(' ')[1] 
                RefreshToken(token).blacklist()
                print('Token has been blacklisted successfully.')
            except Exception as e:
                print(f'Error blacklisting token: {e}')
                return JsonResponse({'error': 'خطأ في حذف التوكن.'}, status=400)
        else:
            print('No refresh token provided.')
            return JsonResponse({'error': 'No refresh token provided.'}, status=400)

        return JsonResponse({'success': True}, status=200)
      
                
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
            expiration_time = timezone.now() + timedelta(minutes=15)
            # إرسال البريد الإلكتروني
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
                    # التحقق من وجود المستخدم مع الرمز والتحقق من انتهاء الصلاحية
            user = CustomUser.objects.filter(
                email=email,
                verification_code=verify_code,
                verification_code_expiry__gt=timezone.now()
            ).first()            
            if not user:
                messages.error(request, "الكود غير صحيح")
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
              if not user:
                  messages.error(request, "انتهت صلاحية الكود")
                  return redirect("forgot-password")
                
              user.password = make_password(new_password)
              user.save()
              request.session['email'] = None
              return redirect('login')
              
          return redirect("reset-password")

def forgotPassword(request):
  return render(request, "forgot_password.html")

def send_code_by_email(request):  
  return render(request, "email_message.html")


class GoogleLoginView(APIView):
    def post(self, request):
        id_token_str = request.data.get('id_token')

        if not id_token_str:
            return Response({'error': 'No id_token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # تحقق من الرمز المميز مع جوجل
            id_info = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                'YOUR_CLIENT_ID.apps.googleusercontent.com'
            )

            # استخراج المعلومات من id_info
            email = id_info.get('email')
            first_name = id_info.get('given_name')
            last_name = id_info.get('family_name')
            google_id = id_info.get('sub')
            picture = id_info.get('picture')
            provider='google'

            if not email:
                return Response({'error': 'Email not available'}, status=status.HTTP_400_BAD_REQUEST)

            # البحث عن المستخدم أو إنشاؤه
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'profile_picture': picture,
                    'password': CustomUser.objects.make_random_password(),
                    'auth_provider':provider,
                    'is_verified':True
                }
            )

            # تحديث معلومات المستخدم إذا لزم الأمر
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.auth_provider = provider
                user.profile_picture = picture
                user.is_verified = True
                user.save()

            # توليد رموز JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_picture': user.profile_picture,
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
          
          
          
          
def googlepage(request):
  return render(request, "auth/trygoogle.html")