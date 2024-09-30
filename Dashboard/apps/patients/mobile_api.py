import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer

class PlanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        plan = SubscriptionPlan.objects.all()
        plan_serializer = SubscriptionPlanSerializer(plan, many=True, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم جلب بيانات الباقات بنجاح',
            'data': plan_serializer.data
        })

