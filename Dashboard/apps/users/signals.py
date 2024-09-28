from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import CustomUser
from apps.users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def user_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            notify.send(instance.first_name, recipient=admin, verb='تم إضافة مستخدم جديد', description=f'تم إضافة {instance.first_name} كامستخدم جديد', action_object=instance,category='User')
