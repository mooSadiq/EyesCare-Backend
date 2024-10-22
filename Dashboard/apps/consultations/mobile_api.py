from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from config import settings
from apps.chat.models import Conversation, Message, File
from .models import Consultation
from apps.chat.serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.models import CustomUser
from apps.doctor.models import Doctor
from apps.patients.models import Patient
from django.db import transaction
import pusher
pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  cluster=settings.PUSHER_CLUSTER,
  ssl=settings.PUSHER_SSL
)

class ConsultationSendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
      try:
          usersender = request.user
          content = request.data.get('content', '') 
          receiver_id = request.data.get('receiver')
          file = request.FILES.get('file')
          print(f"reciever is :{usersender}")
          print(f"reciever is :{receiver_id}")
          print(f"content is :{content}")
          if not content and not file:
              return Response({'error': 'Content or file is required.'}, status=status.HTTP_400_BAD_REQUEST)

          if not receiver_id:
              return Response({'error': 'Doctor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

          try:
              doctor = Doctor.objects.get(id=receiver_id)
              user_doctor = doctor.user
              print(user_doctor)
          except Doctor.DoesNotExist:
              return Response({'error': 'Doctor does not exist.'}, status=status.HTTP_404_NOT_FOUND)
          patient, created = Patient.objects.get_or_create(user=request.user)
          if created:
              user_type = request.user.user_type  
              if user_type != 'admin':
                  request.user.user_type = 'patient'  
                  request.user.save()

          conversation, created = Conversation.objects.get_or_create(
                  user1=user_doctor if request.user.id > user_doctor.id else request.user,
                  user2=request.user if request.user.id > user_doctor.id else user_doctor
          )
          consulation = Consultation.objects.create(
                  patient=patient,
                  doctor=doctor
          )

          with transaction.atomic():
              message_data = {
                'conversation': conversation.id,
                'sender': request.user.id
                }

              if content:
                message_data['content'] = content
              serializer = MessageSerializer(data=message_data, context={'request': request})
              if serializer.is_valid():
                  serializer.save(sender=request.user)
                  message = serializer.instance
                  if file:
                    File.objects.create(message=message, file=file)
                  pusher_client.trigger(f'conversation-{conversation.id}', 'new-message', {
                    'message': MessageSerializer(message).data
                  })
                  return Response({
                      'status': True,
                      'code': status.HTTP_201_CREATED,
                      'message': 'تم ارسال الاستشارة بنجاح',
                    })
              return Response({
                      'status': False,
                      'code': status.HTTP_400_BAD_REQUEST,
                      'message': f'فشل ارسال الاستشارة {serializer.errors}',
                    })
            
      except Exception as e:
            return Response({
                'status': False,
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'حدث خطأ غير متوقع: {str(e)}',
              })

