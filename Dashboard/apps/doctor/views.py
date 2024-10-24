from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status

from apps.doctor.serializers import AddDoctorSerializer, DoctorSerializer, UserSerializer
from .models import Doctor
from apps.users.models import CustomUser

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# دوال الانتقال الى الصفحات
def doctors_list(request):
    return render(request, 'doctors_list.html')

def doctorProfile(request, id):
  
  return render(request, 'doctor_profile.html', {"doctor_id":id})

class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        doctor = Doctor.objects.filter(id=pk).first()        
        if doctor is None:
            return Response({"message": "المريض غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
# دوال المعالجة (جلب، تعديل، API)  
@api_view(['GET'])
def get_all_doctors(request):
  doctors = Doctor.objects.all()
  doctor_serializer = DoctorSerializer(doctors, many=True)    
  users = CustomUser.objects.all()
  user_serializer = UserSerializer(users, many=True)    
  return Response({'doctors':doctor_serializer.data,
                   'users':user_serializer.data})
  
@api_view(['GET'])
def get_by_id_doctor(request,pk):
    doctor = get_object_or_404(Doctor,id=pk)
    doctor_serializer = DoctorSerializer(doctor,many=False)
    return Response(doctor_serializer.data)
  

class DeleteDoctorView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        # الحصول على الطبيب باستخدام id من pk
        doctor = get_object_or_404(Doctor, id=pk)
        
        # الحصول على كائن CustomUser المرتبط بالطبيب
        user = doctor.user
        
        # حذف الطبيب
        delete_result = doctor.delete()
        
        # التحقق من نجاح عملية الحذف
        if delete_result[0] > 0:
            # تحديث نوع المستخدم في CustomUser إلى 'user'
            user.user_type = 'user'
            user.save()
            return Response({"message": "تم الحذف بنجاح!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "لم يتم الحذف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddDoctorView(APIView):
    def post(self, request, *args, **kwargs):
        # الحصول على بيانات الطلب
        user_id = request.data.get('user')
        active_or_not = request.data.get('active_or_not')
        
        # البحث عن المستخدم باستخدام ID
        user = CustomUser.objects.filter(id=user_id).first()
    
        
        # التحقق من وجود المستخدم
        if not user:
            return Response({"success": True, "message": "لم يتم العثور على المستخدم"}, status=status.HTTP_404_NOT_FOUND)

        # # التحقق مما إذا كان المستخدم موجودًا بالفعل كطبيب
        if hasattr(user, 'doctor'):
            return Response({"success": True,"message": "هذا المستخدم موجود في جدول الاطباء"}, status=status.HTTP_400_BAD_REQUEST)

        # تحديث نوع المستخدم إلى 'doctor' وتحديث حالة النشاط
        user.user_type = 'doctor'
        # user.is_active = active_or_not
        user.save()
        
        # حذف 'active_or_not' من البيانات قبل تمريرها إلى الـ Serializer
        doctor_data = request.data.copy()
        # doctor_data.pop('active_or_not', None)
        
        # تهيئة الـ Serializer
        serializer = AddDoctorSerializer(data=doctor_data)
        
        # التحقق من صحة البيانات
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "تم اضافة بيانات الطبيب بنجاح"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
     
@api_view(['PUT'])
def update_doctor(request, id):
    try:
        # الحصول على كائن الطبيب من قاعدة البيانات باستخدام الـ ID
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        return Response({'error': 'الطبيب المراد تحديث بياناته لم يعد موجوداً'}, status=status.HTTP_404_NOT_FOUND)
    
    # تحديث بيانات الطبيب
    data = request.data
    doctor.specialization = data.get('specialization', doctor.specialization)
    doctor.hospital = data.get('hospital', doctor.hospital)
    doctor.address = data.get('address', doctor.address)
    
    # حفظ التغييرات
    doctor.save()
    
    # تسلسل البيانات المعادة للاستجابة
    serializer = DoctorSerializer(doctor, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)