import random
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from config import settings
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import CustomUser  
from apps.patients.models import Patient
from apps.doctor.models import Doctor
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import secrets
from rest_framework.views import APIView
from .serializers import UserCreateSerializer,PasswordResetSerializer

# دالة لتوليد كود تحقق من ستة ارقام
def generate_verification_code():
    return secrets.randbelow(900000) + 100000

def send_verification_email(email, verification_code):
    subject = 'رمز التحقق الخاص بك'
    message = f'رمز التحقق الخاص بك هو: {verification_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
  
    
# View for registering a new user
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        # التحقق مما إذا كان المستخدم موجوداً بالفعل
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if user.is_verified:
                return Response({
                    'message': 'هذا الحساب موجود مسبقا .',
                    'status': False,
                    'code': status.HTTP_400_BAD_REQUEST
                })
            else:
                # إذا كان الحساب غير مفعل، تحديث كود التحقق ومدة صلاحيته
                verification_code = generate_verification_code()
                encrypted_verification_code = make_password(str(verification_code))
                user.verification_code = verification_code
                user.verification_code_expiry = timezone.now() + timedelta(minutes=15)
                user.save()
                send_verification_email(email, verification_code)

                return Response({
                    'message': 'تم ارسال كود التحقق إلى ايميلك .',
                    'status': True,
                    'code': status.HTTP_200_OK
                })
        else:
            # إذا كان البريد الإلكتروني غير موجود، إنشاء مستخدم جديد
            verification_code = generate_verification_code()
            expiration_time = timezone.now() + timedelta(minutes=15)
            encrypted_verification_code = make_password(str(verification_code))
            CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                user_type='user',
                verification_code=verification_code,
                verification_code_expiry=expiration_time
            )
            send_verification_email(email, verification_code)

            return Response({
                'message': 'تم ارسال كود التحقق إلى  ايميلك.',
                'status': True,
                'code': status.HTTP_200_OK
            })        
        
        
# View for verifying the email verification code
class VerifyEmailApiCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')

        user = CustomUser.objects.filter(
            email=email,
            is_verified=False,
            verification_code = code,
            verification_code_expiry__gt=timezone.now()
        ).first()
        if not user:
            return Response({
                'message': 'الكود خطا او انتهت صلاحيته',
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST
            })

        user.is_verified = True
        user.verification_code = ""  # أو None
        user.verification_code_expiry = None
        user.save()

        refresh = RefreshToken.for_user(user)

        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
        }

        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم إنشاء الحساب بنجاح',
            'data': user_data,
        })


# View for logging in the user
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'refresh': str(refresh),
                'access_token': str(refresh.access_token),
            }

            if user.user_type == 'patient':
                patient_data = Patient.objects.get(user=user)
                user_data.update({
                    'patient_id': patient_data.id,
                    'subscription_count': patient_data.subscription_count,
                    'subscription_status': patient_data.subscription_status,
                })

            elif user.user_type == 'doctor':
                doctor_data = Doctor.objects.get(user=user)
                user_data.update({
                    'doctor_id': doctor_data.id,
                    'address': doctor_data.address,
                    'hospital': doctor_data.hospital,
                    'specialization': doctor_data.specialization,
                    'about': doctor_data.about,
                })

            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'نجح تسجيل الدخول',
                'data': user_data,
            })

        return Response({
            'message': 'تأكد من البريد الالكتروني أو كلمة المرور',
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED
        })


# View for handling password reset request
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
            email = request.data.get('email')
            verification_code = generate_verification_code()
            expiration_time = timezone.now() + timedelta(minutes=15)
            encrypted_verification_code = make_password(str(verification_code))
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.verification_code = verification_code
                user.verification_code_expiry = expiration_time
                user.save()
                send_verification_email(email, verification_code)

                return Response({
                    'message': 'تم ارسال كود التحقق الى ايميلك',
                    'status': True,
                    'code': status.HTTP_200_OK
                })

            return Response({
                'message': 'المستخدم غير موجود',
                'status': False,
                'code': status.HTTP_404_NOT_FOUND
            })



# View for verifying the password reset code
class VerifyApiCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')

        user = CustomUser.objects.filter(
            email=email,
            verification_code = code,
            verification_code_expiry__gt=timezone.now()
        ).first()

        if not user:
            return Response({
                'message': 'الكود خطا او انتهت صلاحيته',
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST
            })
        request.session['email'] = email

        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم التحقق بنجاح',
            'data': {},
        })


# View for setting a new password after verification
class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')
        
        if email and new_password:
            user = CustomUser.objects.filter(email=email).first()            
            if user:
                user.password = make_password(new_password)
                user.verification_code = "" 
                user.verification_code_expiry = None
                user.save()
                request.session['email'] = None
                return Response({
                    "message": "تم تغيير كلمة المرور بنجاح.",
                    "status": True,
                    'code': status.HTTP_200_OK
                })
            else:
                return Response({
                    "message": "الجلسة منتهية.",
                    "status": False,
                    'code': status.HTTP_400_BAD_REQUEST
                })
        
        return Response({
            "message": "حدث خطأ.",
            "status": False,
            'code': status.HTTP_400_BAD_REQUEST
        })
