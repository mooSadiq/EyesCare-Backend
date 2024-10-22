from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Address
from apps.doctor.models import Doctor
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, DoctorProfileSerializer, DoctorUpdateProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction

class CuurentUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      try:        
          user_type = request.user.user_type
          print(user_type)
          if user_type == 'doctor':
              doctor = get_object_or_404(Doctor, user=request.user)  
              profile_serializer = DoctorProfileSerializer(doctor, many=False, context={'request': request})
          else :
              profile_serializer = UserProfileSerializer(request.user, many=False, context={'request': request})        
          return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'success',
            'data': profile_serializer.data})
          
      except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"حدث خطأ غير متوقع: {str(e)}"
            })


class UpdateProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        user_serializer = UserProfileSerializer(user, data=request.data, partial=True)
        governorate = request.data.get('user_address')

        try:
          with transaction.atomic():
            if governorate:
                address, created = Address.objects.get_or_create(user=user)
                address.governorate = governorate
                address.save()
            if user.user_type == 'doctor':
                doctor = get_object_or_404(Doctor, user=user)
                print(request.data)
                doctor_serializer = DoctorUpdateProfileSerializer(doctor, data=request.data, partial=True)

                if user_serializer.is_valid():
                    if doctor_serializer.is_valid():
                        self.update_profile_picture(user, request)
                        user_serializer.save()
                        doctor_serializer.save()
                        return Response({
                            'status': True,
                            'code': status.HTTP_200_OK,
                            'message': "تم تعديل بياناتك بنجاح",
                            'data': doctor_serializer.data
                        })
                    else:
                        return Response({
                            'status': False,
                            'code': status.HTTP_400_BAD_REQUEST,
                            'message': f"doctor_errors: {doctor_serializer.errors}"
                        })  

                else:
                    return Response({
                        'status': False,
                        'code': status.HTTP_400_BAD_REQUEST,
                        "message": f"user_errors: {user_serializer.errors}"
                    })

            else:
                if user_serializer.is_valid():
                    self.update_profile_picture(user, request)
                    user_serializer.save()

                    return Response({
                        'status': True,
                        'code': status.HTTP_200_OK,
                        "message": "تم تعديل بياناتك بنجاح",
                        'data': user_serializer.data
                    })

                return Response({
                    'status': False,
                    'code': status.HTTP_400_BAD_REQUEST,
                    "message": f"user_errors: {user_serializer.errors}"
                })

        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"حدث خطأ أثناء تحديث البيانات: {str(e)}"
            })

    def update_profile_picture(self, user, request):
        if 'remove_picture' in request.data and request.data['remove_picture'].lower() == 'true':
            user.profile_picture = 'profile_pics/default_profile_picture.png'
        elif 'profile_picture' in request.FILES and request.FILES['profile_picture']:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
      try:
          new_password = request.data.get('password')
          if not new_password:
                return Response({
                    "message": "يجب إدخال كلمة مرور جديدة.",
                    "status": False,
                    'code': status.HTTP_400_BAD_REQUEST
                })
          user = request.user
          user.set_password(new_password)
          user.save()
          return Response({
              "message": "تم تغيير كلمة المرور بنجاح.",
              "status": True,
              'code': status.HTTP_200_OK
          })       

      except Exception as e:
            return Response({
                'message': f'حدث خطأ غير متوقع: {str(e)}',
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR
            })

      
class GovernoratesListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      try:
          governorates = Address.YEMEN_GOVERNORATES
          data = [{"name": gov[0]} for gov in governorates]
          return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              "message": "تم جلب بيانات المحافظات بنجاح",
              'data': data
          })
      except Exception as e:
          return Response({
              'status': False,
              'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
              "message": f"حدث خطأ أثناء جلب البيانات: {str(e)}"
          })
          
          
class CreateUserAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        governorate = request.data.get('city')
        if not governorate:
            return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'اسم المحافظة مطلوب.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        valid_governorates = [gov[0] for gov in Address.YEMEN_GOVERNORATES]
        if governorate not in valid_governorates:
            return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'المحافظة غير مطابقة للبيانات الموجودة.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            address, created = Address.objects.get_or_create(user=request.user)
            address.governorate = governorate
            address.save() 

            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم تحديث العنوان بنجاح.',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)