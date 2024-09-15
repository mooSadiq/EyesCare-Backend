from django.db import models
from apps.patients.models import Patient
from apps.diseases.models import Disease

# Create your models here.
class DiagnosisReport(models.Model):
    diagnosis_result = models.TextField()  # نتيجة التشخيص
    diagnosis_date = models.DateField(auto_now_add=True)  # تاريخ التشخيص
    image = models.ImageField(upload_to='diagnosis_reports/', blank=True, null=True)  # صورة العين
    compeleted = models.BooleanField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return f"{self.patient},{self.diagnosis_date}" 

class mymodel(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to="diag/")
    
    def str(self):
        return self.title