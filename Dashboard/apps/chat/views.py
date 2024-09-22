from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config import settings
from .models import Conversation, Message, File
from .serializers import ConversationSerializer, MessageSerializer,ContactsSerializer, UserSerializer
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
            user_data = ContactsSerializer(user, context={'request': request}).data
            users_with_conversations.append(user_data)
        return Response({'users': users_with_conversations}, status=status.HTTP_200_OK)
      


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