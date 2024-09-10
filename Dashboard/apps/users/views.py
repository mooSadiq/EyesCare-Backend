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
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password

# دوال العرض والانتقال بين الصفحات في الداش بورد
@login_required
def index(request):
  return render(request, 'user_list.html')
def my_account_settings(request):
  return render(request, 'my_account_settings.html')

def userProfile(request, id):
  return render(request, 'user_profile.html', {"user_id": id})



# دوال المعالجة (جلب، تعديل، API)
class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        users_serializer = UserSerializer(users, many=True)  
        return Response({'users':users_serializer.data,}, status=status.HTTP_200_OK)
      
class UserDetailView(APIView):
    def get(self, request, pk):
        user = CustomUser.objects.filter(id=pk).first()        
        if user is None:
            return Response({"message": "المستخدم غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        users_serializer = UserSerializer(user)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
      


# دالة لتعديل بيانات المستخدم بشكل عام
# هذه الدالة يكن استخدامها في تطبيق المستخدمين او المرضى او الاطباء
class UpdateUserView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)        
        if serializer.is_valid():
            if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
                user.profile_picture = request.FILES['profile_picture']
            serializer.save()
            return Response({
                "message": "تم تعديل بيانات المستخدم بنجاح",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        create_serializer = UserCreateSerializer(data=request.data, partial=True)
        if create_serializer.is_valid():
            email = create_serializer.validated_data['email']            
            if CustomUser.objects.filter(email=email).exists():
                return Response({"message": "هذا الايميل موجود مسبقًا "}, status=status.HTTP_400_BAD_REQUEST)            
            user_type = create_serializer.validated_data['user_type']            
            user = CustomUser.objects.create(
                first_name=create_serializer.validated_data['first_name'],
                last_name=create_serializer.validated_data['last_name'],
                email=email,
                password=make_password(create_serializer.validated_data['password']),
                user_type=user_type,
                is_verified=True,
            )            
            if user_type == 'patient':
                Patient.objects.create(user=user)
            elif user_type == 'doctor':
                Doctor.objects.create(user=user)            
            return Response({
                "message": "تم اضافة المستخدم بنجاح",
                "data": create_serializer.data
            }, status=status.HTTP_200_OK)
                    
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
#دالة لتنشيط او الغاء تنشيط المستخدم 
# هذه الدالة يكن استخدامها في تطبيق المستخدمين او المرضى او الاطباء
class UserActivationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        user.is_active = not user.is_active
        user.save()
        message = 'تم تنشيط الحساب بنجاح' if user.is_active else 'تم إلغاء تنشيط الحساب بنجاح'
        return Response({'message': message, 'is_active': user.is_active}, status=status.HTTP_200_OK)
      
      
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)        
        delete_result = user.delete()
        if delete_result[0] > 0:
            return Response({"message": "تم الحذف بنجاح!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "لم يتم الحذف "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      



class CuurentUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      user_serializer = UserSerializer(request.user, many=False)
      return Response(user_serializer.data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
def update_myProfile(request):
    user = request.user
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.gender = data.get('gender', user.gender)
    user.birth_date = data.get('birth_date', user.birth_date)

    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

