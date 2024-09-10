from .models import Disease
from .serializers import DiseasesSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def get_all_diseases(request):
    Diseases=Disease.objects.all()
    serializer=DiseasesSerializer(Diseases,many=True)
    if serializer.data:
        return Response({"status":True,"code":200,"message":"لقد تم جلب البيانات بنجاح","data":serializer.data},status.HTTP_200_OK)
    else :
        return Response({"status":False,"code":404,"message":"لا يوجد أي بيانات"},status.HTTP_404_NOT_FOUND)