from django.db import models
from apps.users.models import CustomUser

# Create your models here.
class Review(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL)
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=0.0)
    comment = models.TextField(max_length=1000,default="",blank=False) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.rating},{self.comment}"