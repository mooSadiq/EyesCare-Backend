from django.contrib import admin
from .models import Patient
# Register your models here.
@admin.register(Patient)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_count', 'subscription_status')