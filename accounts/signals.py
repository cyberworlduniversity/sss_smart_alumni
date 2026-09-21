from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def sync_admin_permissions(sender, instance, **kwargs):
    if instance.role == "ADMIN" and (not instance.is_staff or not instance.is_superuser):
        User.objects.filter(pk=instance.pk).update(is_staff=True, is_superuser=True)
