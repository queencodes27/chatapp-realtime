from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Friends
from .services.friend import create_friends_obj


@receiver(post_save, sender=User)
def create_friends_object(sender, instance, created, **kwargs):
    """
    Create new friends object after the user is created
    """

    if created:
        create_friends_obj(instance)
