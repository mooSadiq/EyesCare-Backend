from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from apps.patients.models import Patient
from apps.doctor.models import Doctor
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, DoctorProfileSerializer, DoctorUpdateProfileSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password

class CuurentUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      user_type = request.user.user_type
      print(user_type)
      if user_type == 'user':
        profile_serializer = UserProfileSerializer(request.user, many=False, context={'request': request})
      elif user_type == 'doctor':
            # استخدم Doctor.objects.get() للحصول على كائن الطبيب
          doctor = get_object_or_404(Doctor, user=request.user)  # احصل على كائن Doctor المرتبط بالـ User
          profile_serializer = DoctorProfileSerializer(doctor, many=False, context={'request': request})
        
      return Response({
        'status': True,
        'code': status.HTTP_200_OK,
        'message': 'success',
        'data': profile_serializer.data})
    

# class UpdateProfileView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#     def put(self, request):
#         user = request.user
#         serializer = UserProfileSerializer(user, data=request.data, partial=True)        
#         if serializer.is_valid():
#             if 'remove_picture' in request.data and request.data['remove_picture'].lower() == 'true':
#                 user.profile_picture = 'profile_pics/default_profile_picture.jpg' 

#             elif 'profile_picture' in request.FILES and request.FILES['profile_picture']:
#                 user.profile_picture = request.FILES['profile_picture']
#             serializer.save()
#             return Response({
#                 'status': True,
#                 'code': status.HTTP_200_OK,
#                 "message": "تم تعديل بياناتك بنجاح",
#                 'data': serializer.data
#             })
        
#         return Response({
#                 'status': False,
#                 'code': status.HTTP_400_BAD_REQUEST,
#                 "message": serializer.errors
#             })


class UpdateProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        user_serializer = UserProfileSerializer(user, data=request.data, partial=True)

        try:
            if user.user_type == 'doctor':
                doctor = get_object_or_404(Doctor, user=user)
                doctor_serializer = DoctorUpdateProfileSerializer(doctor, data=request.data, partial=True)

                if user_serializer.is_valid():
                    if doctor_serializer.is_valid():
                        self.update_profile_picture(user, request)
                        user_serializer.save()
                        doctor_serializer.save()

                        return Response({
                            'status': True,
                            'code': status.HTTP_200_OK,
                            "message": "تم تعديل بياناتك بنجاح",
                            'data': doctor_serializer.data
                        })
                    else:
                        return Response({
                            'status': False,
                            'code': status.HTTP_400_BAD_REQUEST,
                            "message": {
                                'user_errors': user_serializer.errors,
                                'doctor_errors': doctor_serializer.errors
                            }
                        })  

                else:
                    return Response({
                        'status': False,
                        'code': status.HTTP_400_BAD_REQUEST,
                        "message": {
                            'user_errors': user_serializer.errors,
                        }
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
                    "message": user_serializer.errors
                })

        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"حدث خطأ أثناء تحديث البيانات: {str(e)}"
            })

    def update_profile_picture(self, user, request):
        if 'remove_picture' in request.data and request.data['remove_picture'].lower() == 'true':
            user.profile_picture = 'profile_pics/default_profile_picture.jpg'
        elif 'profile_picture' in request.FILES and request.FILES['profile_picture']:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()