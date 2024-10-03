from rest_framework import permissions
from django.utils import timezone

class HasActiveSubscription(permissions.BasePermission):
    """
    Custom permission to check if the user has an active subscription and remaining consultations.
    """
    
    def has_permission(self, request, view):        
        # التأكد من أن المستخدم لديه ملف مريض
        if hasattr(request.user, 'patient'):
            patient = request.user.patient

            # التحقق مما إذا كان لدى المريض اشتراك نشط واستشارات متبقية
            active_subscription = patient.patient_subscription.filter(
                is_active=True,
                end_date__gt=timezone.localtime(),
                remaining_consultations__gt=0  # التأكد من وجود استشارات متبقية
            ).exists()

            return active_subscription

        # إذا لم يكن للمستخدم ملف مريض، فلا يوجد اشتراك
        return False
