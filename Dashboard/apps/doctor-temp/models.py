from django.db import models
from django.conf import settings
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor')
    address = models.CharField(max_length=255) #العنوان
    hospital = models.CharField(max_length=255) # اسم المستشفى او العيادة
    specialization = models.CharField(max_length=255) # التخصص
    about = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
      