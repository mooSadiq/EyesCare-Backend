from django.db import models
from apps.users.models import CustomUser

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    subscription_count = models.IntegerField(default=0)   # حقل عدد الاشتراكات
    subscription_status = models.BooleanField(default=False)   # حقل حالة الاشتراك
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"