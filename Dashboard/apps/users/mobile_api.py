from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from apps.patients.models import Patient
from apps.doctor.models import Doctor
from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password

class CuurentUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      profile_serializer = UserProfileSerializer(request.user, many=False)
      return Response({
        'status': True,
        'code': status.HTTP_200_OK,
        'message': 'success',
        'data': profile_serializer.data})
    

class UpdateProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request):
        user = user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)        
        if serializer.is_valid():
            if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
                user.profile_picture = request.FILES['profile_picture']
            serializer.save()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                "message": "تم تعديل بياناتك بنجاح"
            })
        
        return Response({
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                "message": serializer.errors
            })
