from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    """Creates the Profile Model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    telegram_chat_id = models.CharField(max_length=50, blank=True,
                                        null=True, unique=True)

    def __str__(self):
        return self.display_name if self.display_name else self.user.username
    

# These ensure that whenever a User is created, a Profile is also created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # We set the display_name to username by default to avoid errors
        Profile.objects.create(user=instance, display_name=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
