from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Consultation
from apps.users.models import CustomUser

@receiver(post_save, sender=Consultation)
def consultation_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            patient_name=f'{instance.patient.user.first_name} {instance.patient.user.last_name}'
            doctor_name=f'{instance.doctor.user.first_name} {instance.doctor.user.last_name}'
            notify.send(instance.patient, recipient=admin, verb='تم طلب إستشارة جديدة', description=f'قام المريض {patient_name} بطلب إستشارة من {doctor_name}', action_object=instance,category='Consultation')
