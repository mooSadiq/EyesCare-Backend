from django.db import models
from apps.users.models import CustomUser
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    address = models.CharField(max_length=255) #العنوان
    hospital = models.CharField(max_length=255) # اسم المستشفى او العيادة
    specialization = models.CharField(max_length=255) # التخصص
    about = models.TextField(null=True)
    start_time_work = models.TimeField(null=True) 
    end_time_work = models.TimeField(null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
      
      
      
class City(models.Model):
  name = models.CharField(max_length=30, null=True)
  
  def __str__(self):
     return self.name