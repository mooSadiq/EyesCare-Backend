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
        journal = Journal.objects.all()
        journal_serializer = JournalSerializer(journal, many=True, context={'request': request})
        return Response({
          'status': True,
          'code': status.HTTP_200_OK,
          'message': 'تم جلب البيانات بنجاح',
          'data': journal_serializer.data
        })
    def post(self, request):
        journal_serializer = JournalSerializer(data=request.data)
        if journal_serializer.is_valid():
            journal_serializer.save()
            return Response({
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': 'تمت الاضافة بنجاح',
            }, status=status.HTTP_201_CREATED)
        return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': f'فشل الاضافة : {journal_serializer.errors}',
            }, status=status.HTTP_400_BAD_REQUEST)

class JournalOneListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        journal = Journal.objects.filter(id=pk).first()
        if not journal:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المجلة غير موجودة',
            })
                            
        journal_serializer = JournalSerializer(journal, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'تم جلب البيانات بنجاح',
            'data': journal_serializer.data
        })
        
    def put(self, request, pk):
        journal = get_object_or_404(Journal, id=pk)
        journal_serializer = JournalSerializer(journal, data=request.data, partial=True) 
        if journal_serializer.is_valid():
            journal_serializer.save()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                "message": "تم تعديل بياناتك بنجاح"
            })
            
    def delete(self, request, pk, *args, **kwargs):
        journal = Journal.objects.filter(id=pk).first()
        if not journal:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المجلة غير موجودة',
            })
                            
        journal.delete()
        return Response({
            'status': True,
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'تم حذف المجلة بنجاح',
        })    

class FieldListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        field = Field.objects.all()
        field_serializer = FieldSerializer(field, many=True, context={'request': request})
        return Response({
          'status': True,
          'code': status.HTTP_200_OK,
          'message': 'تم جلب البيانات بنجاح',
          'data': field_serializer.data
        })

class FieldOneListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        field = Field.objects.filter(id=pk).first()
        if not field:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المجال غير موجود',
            })
                            
        field_serializer = FieldSerializer(field, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'تم جلب البيانات بنجاح',
            'data': field_serializer.data
        })
        
    def put(self, request, pk):
        field = get_object_or_404(Field, id=pk)
        field_serializer = FieldSerializer(field, data=request.data, partial=True) 
        if field_serializer.is_valid():
            field_serializer.save()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                "message": "تم تعديل بياناتك بنجاح"
            })
            
    def delete(self, request, pk, *args, **kwargs):
        field = Field.objects.filter(id=pk).first()
        if not field:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المجال غير موجود',
            })
                            
        field.delete()
        return Response({
            'status': True,
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'تم حذف المجال بنجاح',
        })      
            
class ResearchListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        researches = Research.objects.all()
        researches_serializer = ResearchSerializer(researches, many=True, context={'request': request})
        return Response({
          'status': True,
          'code': status.HTTP_200_OK,
          'message': 'تم جلب البيانات بنجاح',
          'data': researches_serializer.data
        })

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

class ResearchAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        researches = Research.objects.get(id=pk)
        serializer = ResearchOneSerializer(researches, context={'request': request})
        return Response(serializer.data)

      
class ResearchCreatetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ResearchSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  


class JournalCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = JournalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
def research_view(request):
  return render(request, 'research_list.html')
def category_view(request):
  return render(request, 'category_list.html')
def journals_view(request):
  return render(request, 'journal_list.html')