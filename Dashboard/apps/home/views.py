from django.shortcuts import redirect, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request): 
    return render(request, 'dashboard.html')

