from .models import Disease
from .serializers import DiseasesSerializer, DiseaseArabicSerializer, DiseaseEnglishSerializer, DiseaseTrySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .filters import DiseaseFilter

class CustomPagination(PageNumberPagination):
    page_size = 15 
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(data)

class DiseaseListView(APIView):
  pagination_class = CustomPagination
  filterset_class = DiseaseFilter
  permission_classes = [AllowAny]
  
  def get(self, request, *args, **kwargs):
      accept_language = request.headers.get('Accept-Language', 'ar')
      print(accept_language)
      Diseases = Disease.objects.all()
      disease_filter  = self.filterset_class(request.query_params, queryset=Diseases)
      if not disease_filter .is_valid():
          return Response({'message': 'معلمات الفلترة غير صحيحة تأكد منها!'}, status=400)
        
      filtered_diseases  = disease_filter.qs.order_by('id')
      paginator = self.pagination_class()
      paginated_diseases = paginator.paginate_queryset(filtered_diseases, request)
      if accept_language == 'en':
          serializer = DiseaseEnglishSerializer(paginated_diseases,many=True, context={'request': request})
      else:
        serializer = DiseaseTrySerializer(paginated_diseases,many=True, context={'request': request})
         
      return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'ok',
            'data': serializer.data
        })


class DiseaseListSearchView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
      accept_language = request.headers.get('Accept-Language', 'ar')
      Diseases = Disease.objects.all().order_by('id')
      if accept_language == 'en':
          serializer = DiseaseEnglishSerializer(Diseases, many=True, context={'request': request})
      else:
        serializer = DiseaseArabicSerializer(Diseases, many=True, context={'request': request})
         
      return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'ok',
            'data': serializer.data
        })
