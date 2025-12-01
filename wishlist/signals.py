from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wishlist

@receiver(post_save, sender=User)
def create_default_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(
            user=instance,
            title="Default Wishlist"
        )
