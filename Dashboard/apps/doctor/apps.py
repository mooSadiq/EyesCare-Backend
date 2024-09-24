from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.doctor'
    def ready(self):
        import apps.doctor.signals
