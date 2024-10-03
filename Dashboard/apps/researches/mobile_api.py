from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Research, Journal, Field
from rest_framework.parsers import MultiPartParser, FormParser
from .filters import ResearchFilter
from rest_framework.exceptions import ValidationError
from .serializers import ResearchSerializer, JournalSerializer, FieldSerializer, ResearchOneSerializer
# Create your views here.
class JournalListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            journal = Journal.objects.all()
            journal_serializer = JournalSerializer(journal, many=True, context={'request': request})
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'data': journal_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            })
  

class FieldListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            fields = Field.objects.all()
            field_serializer = FieldSerializer(fields, many=True, context={'request': request})
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'data': field_serializer.data
              })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })


          
class ResearchListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            researches = Research.objects.all()
            researches_serializer = ResearchSerializer(researches, many=True, context={'request': request})
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': researches_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })
            
class ResearchFilterListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            researches = Research.objects.all()        
            research_filter = ResearchFilter(request.query_params, queryset=researches)
            if not research_filter.is_valid():
                return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': f'تم تمرير معلمات غير صحيحة بالشكل التالي: {ValidationError(research_filter.errors)}'
                })                  
            queryset = research_filter.qs
            if not queryset.exists():
                return Response({
                  'status': False,
                  'code': status.HTTP_404_NOT_FOUND,
                  'message': 'لم يتم العثور على أي نتائج تطابق الفلترة.'
                })
            research_serializer = ResearchSerializer(queryset, many=True, context={'request': request})
  
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': research_serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })

class ResearchOneListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            research = Research.objects.filter(id=pk).first()
            if not research:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'الدراسة غير موجودة',
                  }, status=status.HTTP_404_NOT_FOUND)
            research_serializer = ResearchOneSerializer(research, context={'request': request})
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'data': research_serializer.data,
            })
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })
