from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Consultation
from django.contrib.auth.models import User

@receiver(post_save, sender=Consultation)
def consultation_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = User.objects.filter(is_staff=True)
        for admin in admin_users:
            notify.send(instance.patient, recipient=admin, verb='تم طلب إستشارة جديدة', description=f'قام المريض{instance.patient} بطلب إستشارة من {instance.doctor}', action_object=instance)
