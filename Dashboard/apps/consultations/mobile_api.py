from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from config import settings
from apps.chat.models import Conversation, Message, File
from .models import Consultation
from apps.chat.serializers import ConversationSerializer, MessageSerializer,ContactsSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.models import CustomUser
from apps.doctor.models import Doctor
from apps.patients.models import Patient
from django.db import transaction


class ConversationList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)
        serializer = ConversationSerializer(conversations, many=True, context={'request': request})
        return Response(serializer.data)
      
    def delete(self, request, pk):
      try:
          conversation = Conversation.objects.get(id=pk)
      except Conversation.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      conversation.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

class ConversationDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            conversation = Conversation.objects.get(
                Q(id=pk) & (Q(user1=request.user) | Q(user2=request.user))
            )
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)

        other_user = conversation.user1 if conversation.user1 != request.user else conversation.user2
        # conversation.messages.filter(is_read=False, sender=other_user).update(is_read=True)

        messages = conversation.messages.filter(is_read=False, sender=other_user)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)
      
    #دالة اغلاق المحادثة   
    def post(self, request, pk):
        try:
            conversation = Conversation.objects.get(
                Q(id=pk) & (Q(user1=request.user) | Q(user2=request.user))
            )
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)
        user_type = request.user.user_type
        if user_type == 'doctor':
            conversation.is_active = False
            conversation.save()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'تم إغلاق المحادثة'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': False,
            'code': status.HTTP_403_FORBIDDEN,
            'message': 'ليس لديك صلاحية إغلاق المحادثة'
        }, status=status.HTTP_403_FORBIDDEN)
        
  
class ConsultationSendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
      try:
          content = request.data.get('content', '') 
          receiver_id = request.data.get('receiver')
          file = request.FILES.get('file')
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
