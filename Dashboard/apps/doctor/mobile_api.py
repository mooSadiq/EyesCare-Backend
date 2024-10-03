import os
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.doctor.models import Doctor, City
from apps.users.models import CustomUser  
from .filters import DoctorFilter
from .serializers import DoctorListSerializer, DoctorOneSerializer, CitySerializer
from rest_framework.exceptions import ValidationError


class DoctorView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        userId = request.data.get('userId')
   
        
        try:
         user = get_object_or_404(CustomUser, id=userId) #authenticate(request, id = userId)
            
         if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'profile_picture':user.profile_picture.url if user.profile_picture else None,  # إرجاع رابط الصور
                'refresh': str(refresh),
                'access_token': str(refresh.access_token),
            }

            if user.user_type == 'doctor':
                doctor_data = Doctor.objects.get(user=user)
                user_data.update({
                    'doctor_id': doctor_data.id,
                    'address': doctor_data.address,
                    'about': doctor_data.about,
                    
                    
                })

            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': '  تم جلب بيانات الطبيب بنجاح',
                'data': user_data,
            })
        except Exception as e:
            
                return Response({
            'message': 'لا توجد بيانات',
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED
             })


class DoctorListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            doctors = Doctor.objects.all()
            doctors_serializer = DoctorListSerializer(doctors, many=True, context={'request': request})
            
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': doctors_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })
            
class DoctorFilterListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            doctors = Doctor.objects.all()        
            doctors_filter = DoctorFilter(request.query_params, queryset=doctors)
            if not doctors_filter.is_valid():
                return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': f'تم تمرير معلمات غير صحيحة بالشكل التالي: {ValidationError(doctors_filter.errors)}'
                })                  
            queryset = doctors_filter.qs
            if not queryset.exists():
                return Response({
                  'status': False,
                  'code': status.HTTP_404_NOT_FOUND,
                  'message': 'لم يتم العثور على أي نتائج تطابق الفلترة.'
                })
            doctors_serializer = DoctorListSerializer(queryset, many=True, context={'request': request})
  
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': doctors_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })            


class CityListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            cities = City.objects.all()
            cities_serializer = CitySerializer(cities, many=True, context={'request': request})
            
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': cities_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })
    
class DoctorOneListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            doctor = Doctor.objects.filter(id=pk).first()
            print('before',type(doctor.start_time_work)) 
            if not doctor:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'الطبيب غير موجود',
                  }, status=status.HTTP_404_NOT_FOUND)
            doctor_serializer = DoctorOneSerializer(doctor, context={'request': request})
            print('after',type(doctor_serializer.data['start_time_work']))
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': doctor_serializer.data,
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })
    
    
class DoctorsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # جلب جميع الأطباء
            doctors = Doctor.objects.all()
            doctor_list = []

            for doctor in doctors:
                user = doctor.user  # الحصول على المستخدم المرتبط بالطبيب
                doctor_data = {
                    'id': user.id,
                    'name': f"{user.first_name} {user.last_name}",  # دمج الاسم الأول والأخير
                    'address': doctor.address,
                    'profile_picture':user.profile_picture.url if user.profile_picture else None,  # إرجاع رابط الصورة
                }
                doctor_list.append(doctor_data)

            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب بيانات الأطباء بنجاح',
                'data': doctor_list,
            })
        except Exception as e:
            return Response({
                'message': 'لا توجد بيانات',
                'status': False,
                'code': status.HTTP_401_UNAUTHORIZED
            })