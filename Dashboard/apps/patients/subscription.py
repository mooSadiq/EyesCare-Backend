import datetime
from django.utils import timezone
from .models import Patient, PatientSubscription, SubscriptionPlan
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

      
class SubscribeToPlan(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            patient, created = Patient.objects.get_or_create(user=request.user)
            if created:
                request.user.user_type = 'patient'  
                request.user.save()
            try:
                plan = SubscriptionPlan.objects.get(id=pk)
            except SubscriptionPlan.DoesNotExist:
                return Response({
                  'status': False,
                  'code': status.HTTP_404_NOT_FOUND,
                  'message': "Invalid subscription plan."}, status=status.HTTP_404_NOT_FOUND)

            # تحديد تاريخ الانتهاء بناءً على الباقة المختارة
            if plan.id == 1:
                end_date = timezone.now() + datetime.timedelta(days=1)
            elif plan.id == 2:
                end_date = timezone.now() + datetime.timedelta(weeks=1)
            elif plan.id == 3:
                end_date = timezone.now() + datetime.timedelta(days=30)
            else:
                return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': "Invalid plan duration."}, status=status.HTTP_400_BAD_REQUEST)

            # التحقق من حالة الاشتراك الحالي
            existing_subscription = PatientSubscription.objects.filter(patient=patient, is_active=True).first()
            if existing_subscription:
                return Response({
                  'status': False,
                  'code': status.HTTP_400_BAD_REQUEST,
                  'message': "You already have an active subscription."}, status=status.HTTP_400_BAD_REQUEST)

            # إنشاء اشتراك جديد للمريض
            patient_subscription = PatientSubscription.objects.create(
                patient=patient,
                plan=plan,
                end_date=end_date,
                is_active=True,
                remaining_consultations=plan.consultation_count  
            )

            patient.subscription_status = True
            patient.subscription_count += 1
            patient.save()
            
            return Response({
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': 'Subscription created successfully!',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
              'status': False,
              'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
              'message': "Failed to create subscription.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      


def check_and_expire_subscriptions():
    expired_subscriptions = PatientSubscription.objects.filter(end_date__lt=timezone.now(), is_active=True)
    for subscription in expired_subscriptions:
        subscription.is_active = False
        subscription.save()
