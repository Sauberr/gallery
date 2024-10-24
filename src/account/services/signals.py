from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from account.models import Profile
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def profile_create(sender, instance, created, **kwargs) -> None:
    if created:
        user = instance
        profile = Profile.objects.create(user=user)


@receiver(post_delete, sender=get_user_model())
def profile_delete(sender, instance, **kwargs) -> None:
    try:
        user = instance.profile
        user.delete()
    except Profile.DoesNotExist:
        pass
