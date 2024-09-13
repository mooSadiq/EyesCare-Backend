from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.

def index(request):
  return render(request, 'advertisements_list.html')
  # return render(request, 'advertisement_details.html')
#جلب الاعلانات
class AdvertisementListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        advertisement = Advertisement.objects.all()
        advertisement_serializer = AdvertisementSerializer(advertisement, many=True)
        
        return Response({'advertisement': advertisement_serializer.data}, status=status.HTTP_200_OK)
      
# جلب البيانات
# @api_view(['GET'])
# def get_advertisements():
#     # جلب جميع الإعلانات من قاعدة البيانات
#     advertisements = Advertisement.objects.all()
#     # advertisements = Advertisement.objects #.filter(status=True)  # جلب الإعلانات النشطة فقط
    
#     # return render(request, 'advertisements_list.html',{'advertisements': advertisements})
    
#     # تسلسل البيانات باستخدام AdvertisementSerializer
#     serializer = AdvertisementSerializer(advertisements, many=True)
    
#     # إعادة الاستجابة كـ JSON
#     return Response({'advertisement':"hellllllllllllo"}, status=status.HTTP_200_OK)

#اضافة اعلان
class AdvertisementImageUploadView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # إنشاء السيراليزر باستخدام البيانات الواردة من الطلب
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            # حفظ البيانات باستخدام السيراليزر لضمان تطبيق كافة التحقق
            newA = serializer.save()
            advert = AdvertisementSerializer(newA, many=False)
            return Response({"success": "تم حفظ البيانات بنجاح", "message": advert.data}, status=status.HTTP_201_CREATED)
        else:
            # إعادة أخطاء التحقق في الرد
            return Response({"message": "البيانات غير صحيحة", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# دال تحديث اعلان
@api_view(['PATCH'])
def update_advertisement(request, pk):
    try:
        # جلب الإعلان المطلوب من قاعدة البيانات
        advertisement = Advertisement.objects.get(pk=pk)
    except Advertisement.DoesNotExist:
        return Response({'error': 'الإعلان غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    # تسلسل البيانات المحدثة باستخدام AdvertisementSerializer
    serializer = AdvertisementSerializer(advertisement, data=request.data, partial=True)
    
    # التحقق من صحة البيانات
    if serializer.is_valid():
        serializer.save()  # حفظ التحديثات في قاعدة البيانات
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
# دالة حذف الاعلان
@api_view(['DELETE'])
def delete_advertisement(request, pk):
    try:
        # جلب الإعلان المطلوب من قاعدة البيانات
        advertisement = Advertisement.objects.get(pk=pk)
    except Advertisement.DoesNotExist:
        return Response({'error': 'الإعلان غير موجود'}, status=status.HTTP_404_NOT_FOUND)
    
    # حذف الإعلان
    advertisement.delete()
    return Response({'message': 'تم حذف الإعلان بنجاح'}, status=status.HTTP_200_OK)