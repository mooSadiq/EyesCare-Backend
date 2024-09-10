from django.db import models

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=255)  # اسم المرض
    description = models.TextField()  # وصف المرض
    image = models.ImageField(upload_to='diseases_images/', blank=True, null=True)  # صورة المرض
    causes = models.TextField()  # الأسباب
    symptoms = models.TextField()  # الأعراض
    diagnosis_methods = models.TextField()  # طرق التشخيص
    treatment_options = models.TextField()  # خيارات العلاج
    prevention_recommendations = models.TextField()  # توصيات الوقاية
    status=models.TextField(default="ليس متاحاً للتشخيص")
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name 
