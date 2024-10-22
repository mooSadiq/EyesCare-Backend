from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config import settings
from .models import Conversation, Message, File
from .serializers import MessageSendSerializer, MessageSerializer,ContactsTrySerializer, UserSerializer, ConversationDetailSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.models import CustomUser
from django.db import transaction
import pusher
from django.db.models import Q

pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  cluster=settings.PUSHER_CLUSTER,
  ssl=settings.PUSHER_SSL
)
# Create your views here.

def chatview(request):
  return render(request, 'chat.html')

class UsersListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.all()
        users_serializer = UserSerializer(users, many=True)  
        return Response({'users':users_serializer.data,}, status=status.HTTP_200_OK)

class ContactsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.all()        
        users_with_conversations = []
        for user in users:
            user_data = ContactsTrySerializer(user, context={'request': request}).data
            users_with_conversations.append(user_data)
        return Response({'users': users_with_conversations}, status=status.HTTP_200_OK)
      
class ConversationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            conversation = Conversation.objects.get(
                Q(id=pk) & (Q(user1=request.user) | Q(user2=request.user))
            )
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationDetailSerializer(conversation, context={'request': request})
        return Response(serializer.data)
      
class MessageList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        content = request.data.get('content', '') 
        receiver_id = request.data.get('receiver')
        file = request.FILES.get('file')
        print(f"content is: {content}, receiver id: {receiver_id}, file is {file}")
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
            serializer = MessageSendSerializer(data=message_data, context={'request': request})
            print('seril')
            if serializer.is_valid():
                serializer.save(sender=request.user)
                message = serializer.instance
                print(message)
                if file:
                  File.objects.create(message=message, file=file)
                pusher_client.trigger(f'conversation-{conversation.id}', 'new-message', {
                    'message': MessageSerializer(message).data
                })


                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MessageReceived(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            message = Message.objects.get(id=pk, conversation__user1=request.user) | Message.objects.get(id=pk, conversation__user2=request.user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)

        if not message.is_received:
            message.is_received = True
            message.save()

        return Response({'status': 'Message marked as received'}, status=status.HTTP_200_OK)