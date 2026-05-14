from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile


@receiver(post_save, sender=get_user_model())
def profile_create(sender, instance, created, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)
