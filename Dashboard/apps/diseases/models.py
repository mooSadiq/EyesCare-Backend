from django.db import models

# Create your models here.
class Disease(models.Model):
    name_ar = models.CharField(max_length=255)  # اسم المرض
    name_en = models.CharField(max_length=255)  
        
    description_ar = models.TextField()  # وصف المرض 
    description_en = models.TextField(null=True) 
    
    image = models.ImageField(upload_to='diseases_images/', blank=True, null=True)  # صورة المرض
    causes_paragraph_ar = models.TextField(null=True, blank=True)
    causes_points_ar = models.TextField(null=True, blank=True)
    symptoms_paragraph_ar = models.TextField(null=True, blank=True)
    symptoms_points_ar = models.TextField(null=True, blank=True)
    diagnosis_methods_paragraph_ar = models.TextField(null=True, blank=True)
    diagnosis_methods_points_ar = models.TextField(null=True, blank=True)
    treatment_options_paragraph_ar = models.TextField(null=True, blank=True)
    treatment_options_points_ar = models.TextField(null=True, blank=True)
    prevention_recommendations_paragraph_ar = models.TextField(null=True, blank=True)
    prevention_recommendations_points_ar = models.TextField(null=True, blank=True)
    causes_en = models.JSONField(null=True) 
    
    symptoms_en = models.JSONField(null=True)  
    
    diagnosis_methods_en = models.JSONField(null=True)  
    
    treatment_options_en = models.JSONField(null=True)  
    
    prevention_recommendations_en = models.JSONField(null=True)  
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name_en 
