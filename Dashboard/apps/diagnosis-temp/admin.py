from django.contrib import admin
from .models import DiagnosisReport

# Register your models here.
@admin.register(DiagnosisReport)
class DiagnosisReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis_result', 'diagnosis_date', 'disease')