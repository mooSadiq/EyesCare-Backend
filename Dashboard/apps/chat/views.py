from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.users.models import CustomUser

# Create your views here.

def chatview(request):
  return render(request, 'chat.html')

class UsersListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.all()
        users_serializer = UserSerializer(users, many=True)  
        return Response({'users':users_serializer.data,}, status=status.HTTP_200_OK)
