from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import DiagnosisReport
from apps.users.models import CustomUser

@receiver(post_save, sender=DiagnosisReport)
def diagnosisReport_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            notify.send(instance.patient, recipient=admin, verb='تم إضافة تشخيص جديد', description=f'{instance.diagnosis_result}', action_object=instance,category='DiagnosisReport')
