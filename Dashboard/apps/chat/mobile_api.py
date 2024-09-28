from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from config import settings
from .models import Conversation, Message, File
from .serializers import ConversationSerializer, MessageSerializer,ContactsSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.models import CustomUser
from django.db import transaction
import pusher

pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  cluster=settings.PUSHER_CLUSTER,
  ssl=settings.PUSHER_SSL
)

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
        conversation.messages.filter(is_read=False, sender=other_user).update(is_read=True)

        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)
      
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
        
  
class MessageList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        content = request.data.get('content', '') 
        receiver_id = request.data.get('receiver')
        file = request.FILES.get('file')
        
        if not content and not file:
            return Response({'error': 'Content or file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not receiver_id:
            return Response({'error': 'Receiver ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Receiver does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        conversation, created = Conversation.objects.get_or_create(
                user1=receiver if request.user.id > receiver.id else request.user,
                user2=request.user if request.user.id > receiver.id else receiver
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
                # إرسال إشعار عبر Pusher
                pusher_client.trigger(f'conversation-{conversation.id}', 'new-message', {
                    'message': MessageSerializer(message).data
                })

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


