from rest_framework.views import APIView
from .models import Advertisement
from .serializers import AdvertisementSerializerMobile
from rest_framework import status
from rest_framework.response import Response



class AdvertisementList(APIView):
    def get(self,request):
        advertisement=Advertisement.objects.filter(allowed=True)
        serializer=AdvertisementSerializerMobile(advertisement,many=True,context={'request': request})
        if serializer.data:
            return Response({"status":True,"code":200,"message":"لقد تم جلب البيانات بنجاح","data":serializer.data},status.HTTP_200_OK)
        else:
            return Response({"status":False,"code":404,"Info":"لا يوجد أي بيانات"},status.HTTP_404_NOT_FOUND)


class AddClick(APIView):
    def put(self, request, pk):
        advertisement = Advertisement.objects.filter(id=pk).first() 
        if not advertisement:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'الإعلان غير موجود',
            })
        advertisement.clicks_count += 1
        advertisement.save()
        return Response({
            'status': True,
            'code': 200,
            'message': 'تم الزيادة بنجاح',
        })

class AddViews(APIView):
    def put(self, request, pk):
        advertisement = Advertisement.objects.filter(id=pk).first() 
        if not advertisement:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'الإعلان غير موجود',
            })
        advertisement.views_count += 1
        advertisement.save()
        return Response({
            'status': True,
            'code': 200,
            'message': 'تم الزيادة بنجاح',
        })
