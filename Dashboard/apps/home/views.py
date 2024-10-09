from django.shortcuts import redirect, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count
from . import serializers
# Create your views here.

@login_required
def index(request): 
    return render(request, 'dashboard.html')

class StaticsList(APIView):
    def get(self, request):
        response_data=serializers.doAll()
        return Response(response_data, status=status.HTTP_200_OK)




