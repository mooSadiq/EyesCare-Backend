from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Research, Journal, Field
from .filters import ResearchFilter
from django.db import transaction
from django.db.models import F, Sum
from rest_framework.exceptions import ValidationError
from .serializers import ResearchSerializer, JournalSerializer, FieldSerializer,ResearchListSerializer, ResearchOneSerializer,ResearchCreateSerializer, StatisticsSerializer
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
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request):
        try:
          journal_serializer = JournalSerializer(data=request.data)
          if journal_serializer.is_valid():
              journal_serializer.save()
              return Response({
                  'status': True,
                  'code': status.HTTP_201_CREATED,
                  'message': 'تمت الاضافة بنجاح',
              }, status=status.HTTP_201_CREATED)
          else:
            return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': f'فشل الاضافة : {journal_serializer.errors}',
              }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class JournalOneListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            journal = Journal.objects.filter(id=pk).first()
            if not journal:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجلة غير موجودة',
                }, status=status.HTTP_404_NOT_FOUND)

            journal_serializer = JournalSerializer(journal, context={'request': request})
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'data': journal_serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        try:
            journal = Journal.objects.filter(id=pk).first()
            if not journal:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجلة غير موجودة',
                }, status=status.HTTP_404_NOT_FOUND)
            print(request.data)
            journal_serializer = JournalSerializer(journal, data=request.data, partial=True)
            if journal_serializer.is_valid():
                journal_serializer.save()
                return Response({
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'تم تعديل بيانات المجلة بنجاح'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': f'فشل تعديل بيانات المجلة: {journal_serializer.errors}'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, *args, **kwargs):
        try:
            journal = Journal.objects.filter(id=pk).first()
            if not journal:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجلة غير موجودة',
                }, status=status.HTTP_404_NOT_FOUND)
            journal.delete()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم حذف المجلة بنجاح',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

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
              }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request):
        try:
            field_serializer = FieldSerializer(data=request.data)
            if field_serializer.is_valid():
                field_serializer.save()
                return Response({
                    'status': True,
                    'code': status.HTTP_201_CREATED,
                    'message': 'تم إضافة المجال بنجاح',
                  }, status=status.HTTP_201_CREATED)
            return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': f'فشل إضافة المجال : {field_serializer.errors}',
              }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FieldOneListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            field = Field.objects.filter(id=pk).first()
            if not field:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجال غير موجود',
                  }, status=status.HTTP_404_NOT_FOUND)

            field_serializer = FieldSerializer(field, context={'request': request})
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'data': field_serializer.data
              }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            field = Field.objects.filter(id=pk).first()
            if not field:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجال غير موجود',
                  }, status=status.HTTP_404_NOT_FOUND)

            field_serializer = FieldSerializer(field, data=request.data, partial=True)
            if field_serializer.is_valid():
                field_serializer.save()
                return Response({
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': "تم تعديل بياناتك بنجاح"
                  }, status=status.HTTP_200_OK)
            return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': f'فشل تعديل البيانات: {field_serializer.errors}',
              }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, pk, *args, **kwargs):
        try:
            field = Field.objects.filter(id=pk).first()
            if not field:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'المجال غير موجود',
                  }, status=status.HTTP_404_NOT_FOUND)

            field.delete()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم حذف المجال بنجاح',
              }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
            
class ResearchListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            researches = Research.objects.all()
            journal = Journal.objects.all()
            field = Field.objects.all()

            researches_serializer = ResearchListSerializer(researches, many=True, context={'request': request})
            journal_serializer = JournalSerializer(journal, many=True, context={'request': request})
            field_serializer = FieldSerializer(field, many=True, context={'request': request})

            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'research': researches_serializer.data,
                'journal': journal_serializer.data,
                'field': field_serializer.data
              }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            with transaction.atomic():
                researches_serializer = ResearchCreateSerializer(data=request.data)
                if researches_serializer.is_valid():
                    research = researches_serializer.save(user=request.user)

                    field = research.field
                    field.research_count = F('research_count') + 1
                    field.save(update_fields=['research_count'])

                    journal = research.journal
                    journal.research_count = F('research_count') + 1
                    journal.save(update_fields=['research_count'])

                    return Response({
                        'status': True,
                        'code': status.HTTP_200_OK,
                        'message': 'تم إضافة الدراسة بنجاح',
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': False,
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': f'فشل إضافة الدراسة : {researches_serializer.errors}',
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResearchFilterListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        print(queryset)
        research_serializer = ResearchSerializer(queryset, many=True, context={'request': request})
        
        return Response({
          'status': True,
          'code': status.HTTP_200_OK,
          'message': 'تم جلب البيانات بنجاح',
          'data': research_serializer.data
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
                    'message': 'المجال غير موجود',
                  }, status=status.HTTP_404_NOT_FOUND)
            journal = Journal.objects.all()
            field = Field.objects.all()
            research_serializer = ResearchOneSerializer(research, context={'request': request})
            journal_serializer = JournalSerializer(journal, many=True, context={'request': request})
            field_serializer = FieldSerializer(field, many=True, context={'request': request})
            return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم جلب البيانات بنجاح',
              'research': research_serializer.data,
              'journal': journal_serializer.data,
              'field': field_serializer.data
            })
            
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        try:
          research = Research.objects.filter(id=pk).first()
          if not research:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'الدراسة غير موجودة',
            })
                  # حفظ القيم السابقة للمجلة والمجال وذلك من أجل التحقق هل تم تعديلهم 
          previous_journal = research.journal
          previous_field = research.field
          print(request.data)
          research_serializer = ResearchCreateSerializer(research, data=request.data, partial=True)
          if research_serializer.is_valid():
              updated_research = research_serializer.save(user=request.user)         
              if previous_journal != updated_research.journal:
                previous_journal.research_count = F('research_count') - 1
                previous_journal.save(update_fields=['research_count'])
                updated_research.journal.research_count = F('research_count') + 1
                updated_research.journal.save(update_fields=['research_count'])
                
              if previous_field != updated_research.field:
                previous_field.research_count = F('research_count') - 1
                previous_field.save(update_fields=['research_count'])                    
                updated_research.field.research_count = F('research_count') + 1
                updated_research.field.save(update_fields=['research_count'])
              return Response({
                  'status': True,
                  'code': status.HTTP_200_OK,
                  'message': 'تم تعديل الدراسة بنجاح',
              }, status=status.HTTP_200_OK)
          else:
              return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': f'فشل تعديل الدراسة : {research_serializer.errors}',
              }, status=status.HTTP_400_BAD_REQUEST)
      
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            research = Research.objects.filter(id=pk).first()
            if not research:
                return Response({
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'الدراسة غير موجودة',
                })

            research.delete()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم حذف الدراسة بنجاح',
            }, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
      

class ResearchStatisticsView(APIView):
    def get(self, request):
      try:
          research_count = Research.objects.count()
          field_count = Field.objects.count()
          journal_count = Journal.objects.count()
          total_downloads = Research.objects.aggregate(Sum('downloads_count'))['downloads_count__sum'] or 0
          pdf_count = Research.objects.filter(is_file=True).count()
          no_pdf_count = Research.objects.filter(is_file=False).count()
          data = {
              'research_count': research_count,
              'field_count': field_count,
              'journal_count': journal_count,
              'total_downloads': total_downloads,
              'pdf_count': pdf_count,
              'no_pdf_count': no_pdf_count,
          }
          statistics_serializer = StatisticsSerializer(data)
          return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم جلب البيانات بنجاح',
                'data': statistics_serializer.data,
              }, status=status.HTTP_200_OK)
        
      except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
def research_view(request):
  return render(request, 'research_list.html')
def research_details_view(request, id):
  return render(request, 'research_details.html', {"research_id": id})
def category_view(request):
  return render(request, 'category_list.html')
def journals_view(request):
  return render(request, 'journal_list.html')