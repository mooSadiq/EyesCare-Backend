from rest_framework import permissions
from django.utils import timezone

class HasActiveSubscription(permissions.BasePermission):
    """
    Custom permission to check if the user has an active subscription and remaining consultations.
    """
    
    def has_permission(self, request, view):        
        if hasattr(request.user, 'patient'):
            patient = request.user.patient

            active_subscription = patient.patient_subscription.filter(
                is_active=True,
                end_date__gt=timezone.localtime(),
                remaining_consultations__gt=0  
            ).exists()

            return active_subscription

        return False
