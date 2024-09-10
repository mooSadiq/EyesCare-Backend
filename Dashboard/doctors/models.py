from django.db import models

# Create your models here.
class doctors(models.Model):
    name = models.CharField( help_text="اسم الطبيب", max_length=150 )
    phone = models.IntegerField()
    profile = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    email = models.EmailField(max_length=254, )
    location = models.CharField( max_length=250)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name