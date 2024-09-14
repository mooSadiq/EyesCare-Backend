from django.db import models

# Create your models here.
class Disease(models.Model):
    name_ar = models.CharField(max_length=255)  # اسم المرض
    name_en = models.CharField(max_length=255)  
        
    description_ar = models.TextField()  # وصف المرض 
    description_en = models.TextField(null=True) 
    
    image = models.ImageField(upload_to='diseases_images/', blank=True, null=True)  # صورة المرض
    
    causes_ar = models.JSONField()  # الأسباب 
    causes_en = models.JSONField(null=True) 
    
    symptoms_ar = models.JSONField()  # الأعراض 
    symptoms_en = models.JSONField(null=True)  
    
    diagnosis_methods_ar = models.JSONField()  # طرق التشخيص 
    diagnosis_methods_en = models.JSONField(null=True)  
    
    treatment_options_ar = models.JSONField()  # خيارات العلاج 
    treatment_options_en = models.JSONField(null=True)  
    
    prevention_recommendations_ar = models.JSONField()  # توصيات الوقاية 
    prevention_recommendations_en = models.JSONField(null=True)  
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name_en 
