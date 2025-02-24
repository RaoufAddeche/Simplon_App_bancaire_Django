from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Advisor: a banking advisor assigned to the client.
    advisor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='clients',
        on_delete=models.SET_NULL,
        help_text="Assigned banking advisor"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

# Automatically create a Profile instance when a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
