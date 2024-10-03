from datetime import timezone
from django.db import models
from apps.users.models import CustomUser

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    subscription_count = models.IntegerField(default=0)   # حقل عدد الاشتراكات
    subscription_status = models.BooleanField(default=False)   # حقل حالة الاشتراك
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
      
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=30, null=True)
    consultation_count = models.IntegerField(default=0)  # عدد الاستشارات


class PatientSubscription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,  related_name='patient_subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    remaining_consultations = models.IntegerField(default=0)  # الاستشارات المتبقية في الاشتراك
