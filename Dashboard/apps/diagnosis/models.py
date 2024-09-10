from django.db import models
from apps.patients.models import Patient
from apps.diseases.models import Disease
import uuid
import time
# Create your models here.
class DiagnosisReport(models.Model):
    diagnosis_result = models.TextField()  # نتيجة التشخيص
    diagnosis_date = models.DateTimeField(auto_now_add=True)  # تاريخ التشخيص
    image = models.ImageField(upload_to='diagnosis_reports/', blank=True, null=True)  # صورة العين
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.patient},{self.diagnosis_date}" 

class MyModel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images_try/')  # حفظ الملف في مجلد 'images/' داخل 'MEDIA_ROOT'

    def save(self, *args, **kwargs):
        if self.image:
            extension = self.image.name[self.image.name.rfind('.'):]

            unique_id = int(time.time() * 1000) 
            self.image.name = f"diag_img_{unique_id}{extension}"
        
        super(MyModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title