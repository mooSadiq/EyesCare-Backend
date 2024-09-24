from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Research
from .serializers import ResearchSerializer
# Create your views here.

class ResearchListAPIView(APIView):
    def get(self, request):
        researches = Research.objects.all()
        serializer = ResearchSerializer(researches, many=True)
        return Response(serializer.data)


      
class ResearchCreatetAPIView(APIView):
    def post(self, request):
        serializer = ResearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  