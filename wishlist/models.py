from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="My Wishlist")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    links = models.JSONField(default=list, blank=True)
    priority = models.IntegerField(default=3)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    purchased = models.BooleanField(default=False)
    purchased_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='purchases'
    )
    purchased_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

