from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Consultation
from .serializers import ConsultationSerializer
from django.shortcuts import get_object_or_404, render
import logging
# Create your views here.

def index(request):
    return render(request, 'consultations_list.html')

logger = logging.getLogger(__name__)

class ConsultationListView(APIView):

    def get(self, request):
        try:
            # استرجاع جميع الاستشارات من قاعدة البيانات
            consultations = Consultation.objects.all()

            # تحويل الاستشارات إلى JSON باستخدام الاستيراد
            serializer = ConsultationSerializer(consultations, many=True)
            
            # إرجاع الاستجابة مع البيانات وحالة HTTP 200
            return Response({'consultations': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in ConsultationListView: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ConsultationDetailView(APIView):
    def delete(self, request, pk):
        # جلب الاستشارة المحددة باستخدام المعرف (pk)
        consultation = get_object_or_404(Consultation, pk=pk)
        
        # حذف الاستشارة
        consultation.delete()
        
        # إرجاع استجابة تأكيدية بنجاح الحذف
        return Response({'success': True, 'message': 'استشارة تم حذفها بنجاح'}, status=status.HTTP_200_OK)