from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Review
from apps.users.models import CustomUser

@receiver(post_save, sender=Review)
def review_created_notification(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_staff=True)
        for admin in admin_users:
            notify.send(instance.user, recipient=admin, verb='تم إضافة تقييم جديد', description=f'Rateing: {instance.rating} - Coment:{instance.comment}', action_object=instance,category='Rateing')