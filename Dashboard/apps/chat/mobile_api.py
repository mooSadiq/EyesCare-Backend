from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config import settings
from .models import Conversation, Message, File
from .serializers import ConversationSerializer, MessageSerializer
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
        conversations = Conversation.objects.get(id=pk)
        serializer = ConversationSerializer(conversations, many=False, context={'request': request})
        return Response(serializer.data)

class MessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id, user1_id=request.user) | Conversation.objects.get(id=conversation_id, user2_id=request.user)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)

        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
      
    def post(self, request):
        content = request.data.get('content')
        receiver_id = request.data.get('receiver')
        file = request.FILES.get('file')
        
        if not content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

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
            serializer = MessageSerializer(data={'content': content, 'conversation': conversation.id, 'sender': request.user.id})
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
