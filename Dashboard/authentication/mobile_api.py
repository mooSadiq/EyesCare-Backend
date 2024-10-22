import random
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from config import settings
from django.contrib.auth.hashers import make_password
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
      try:
          first_name = request.data.get('first_name')
          last_name = request.data.get('last_name')
          email = request.data.get('email')
          password = request.data.get('password')
          user = CustomUser.objects.filter(email=email).first()
          if user:
              if user.is_verified:
                  return Response({
                      'message': 'هذا الحساب موجود مسبقا .',
                      'status': False,
                      'code': status.HTTP_400_BAD_REQUEST
                  })
              else:
                  verification_code = generate_verification_code()
                  encrypted_verification_code = make_password(str(verification_code))
                  user.verification_code = verification_code
                  user.verification_code_expiry = timezone.now() + timedelta(minutes=3)
                  user.save()
                  send_verification_email(email, verification_code)
                  if user.first_name != first_name:
                      user.first_name = first_name                
                  if user.last_name != last_name:
                      user.last_name = last_name
                  if not user.check_password(password):
                      user.set_password(password)
                  user.save()
                  return Response({
                      'message': 'تم ارسال كود التحقق إلى ايميلك .',
                      'status': True,
                      'code': status.HTTP_200_OK
                  })
          else:
              verification_code = generate_verification_code()
              expiration_time = timezone.now() + timedelta(minutes=3)
              encrypted_verification_code = make_password(str(verification_code))
              CustomUser.objects.create(
                  first_name=first_name,
                  last_name=last_name,
                  email=email,
                  password=make_password(password),
                  profile_picture = 'profile_pics/default_profile_picture.png',
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
      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })
        
# View for verifying the email verification code
class VerifyEmailApiCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
      try:
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
          user.verification_code = None
          user.verification_code_expiry = None
          user.save()

          refresh = RefreshToken.for_user(user)
          domain = request.get_host()
          profile_picture =  f"http://{domain}{user.profile_picture.url}"
          user_address = user.user_address.governorate if hasattr(user, 'user_address') and user.user_address.governorate else None
          user_data = {
              'id': user.id,
              'email': user.email,
              'first_name': user.first_name,
              'last_name': user.last_name,
              'user_address': user_address,
              'profile_picture': profile_picture,
              'user_type': user.user_type,
              'is_blue_verified': user.is_blue_verified,
              'refresh': str(refresh),
              'access_token': str(refresh.access_token),
          }

          return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم إنشاء الحساب بنجاح',
              'data': user_data,
          })
      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({
                    'message': 'يجب إدخال البريد الإلكتروني وكلمة المرور.',
                    'status': False,
                    'code': status.HTTP_400_BAD_REQUEST
                })

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({
                    'message': 'الحساب غير موجود.',
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND
                })

            if not user.is_verified:
                return Response({
                    'message': 'الحساب غير موجود. ',
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND
                })
            if not user.is_active:
                return Response({
                    'message': 'هذا الحساب غير نشط. ',
                    'status': False,
                    'code': status.HTTP_406_NOT_ACCEPTABLE
                })

            user = authenticate(request, email=email, password=password)
            if user is None:
                return Response({
                    'message': 'تأكد من البريد الالكتروني أو كلمة المرور.',
                    'status': False,
                    'code': status.HTTP_401_UNAUTHORIZED
                })

            refresh = RefreshToken.for_user(user)
            domain = request.get_host()
            profile_picture =  f"http://{domain}{user.profile_picture.url}"
            user_address = user.user_address.governorate if hasattr(user, 'user_address') and user.user_address.governorate else None
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_address': user_address,
                'profile_picture': profile_picture,
                'user_type': user.user_type,
                'is_blue_verified': user.is_blue_verified,
                'refresh': str(refresh),
                'access_token': str(refresh.access_token),
            }

            if user.user_type == 'patient':
                try:
                    patient_data = Patient.objects.get(user=user)
                    user_data.update({
                        'patient_id': patient_data.id,
                        'subscription_count': patient_data.subscription_count,
                        'subscription_status': patient_data.subscription_status,
                    })
                except Patient.DoesNotExist:
                    return Response({
                        'message': 'بيانات المريض غير موجودة.',
                        'status': False,
                        'code': status.HTTP_404_NOT_FOUND
                    })

            elif user.user_type == 'doctor':
                try:
                    doctor_data = Doctor.objects.get(user=user)
                    user_data.update({
                        'doctor_id': doctor_data.id,
                        'address': doctor_data.address,
                        'hospital': doctor_data.hospital,
                        'specialization': doctor_data.specialization,
                        'about': doctor_data.about,
                    })
                except Doctor.DoesNotExist:
                    return Response({
                        'message': 'بيانات الطبيب غير موجودة.',
                        'status': False,
                        'code': status.HTTP_404_NOT_FOUND
                    })
            
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'نجح تسجيل الدخول',
                'data': user_data,
            })

        except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })
            
# View for handling password reset request
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
      try:
          email = request.data.get('email')
          verification_code = generate_verification_code()
          expiration_time = timezone.now() + timedelta(minutes=3)
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
      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })


# View for verifying the password reset code
class VerifyApiCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
      try:
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
      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })


# View for setting a new password after verification
class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
      try:
          email = request.data.get('email')
          new_password = request.data.get('password')

          if email and new_password:
              user = CustomUser.objects.filter(email=email).first()            
              if user:
                  extended_expiry_time = user.verification_code_expiry + timedelta(minutes=5)
                  if extended_expiry_time < timezone.now():
                      return Response({
                          "message": "الجلسة منتهية. يرجى طلب كود تحقق جديد.",
                          "status": False,
                          'code': status.HTTP_400_BAD_REQUEST
                      })
                  user.set_password(new_password)
                  user.verification_code = None 
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
                      "message": "المستخدم غير موجود.",
                      "status": False,
                      'code': status.HTTP_400_BAD_REQUEST
                  })        
          return Response({
              "message": "حدث خطأ.",
              "status": False,
              'code': status.HTTP_400_BAD_REQUEST
          })
      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })


