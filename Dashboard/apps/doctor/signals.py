from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Doctor
from apps.users.models import CustomUser

@receiver(post_save, sender=Doctor)
def doctor_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            notify.send(instance.user, recipient=admin, verb='تم إضافة دكتور جديد', description=f'تم إضافة{instance.user}كادكتور', action_object=instance,category='Doctor')
