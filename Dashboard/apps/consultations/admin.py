from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'is_complete', 'consultation_date')
    list_filter = ('is_complete', 'consultation_date')
    search_fields = ('patient__user__username', 'doctor__user__username')
