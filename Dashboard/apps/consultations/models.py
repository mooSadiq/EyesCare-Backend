from django.db import models

from apps.patients.models import Patient
from apps.doctor.models import Doctor

# Create your models here.
class Consultation(models.Model):
    # نموذج للاستشارة
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')
    is_complete = models.BooleanField(default=False)  # حالة الاستشارة
    consultation_date = models.DateField(auto_now_add=True)  # تاريخ الاستشارة

    def __str__(self):
        return f'Consultation with {self.doctor} on {self.consultation_date}'