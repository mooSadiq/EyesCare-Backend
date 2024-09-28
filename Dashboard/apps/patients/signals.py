from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Patient
from apps.users.models import CustomUser

@receiver(post_save, sender=Patient)
def patient_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            user_name = f"{instance.user.first_name} {instance.user.last_name}".strip()
            notify.send(instance.user, recipient=admin, verb='تم إضافة مريض جديد', description=f'تم إضافة{user_name} كمريض', action_object=instance,category='Patient')
