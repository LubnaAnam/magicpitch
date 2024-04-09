from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User

class User(AbstractUser):
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    registration_timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.username


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    timestamp = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender , instance=None , created=False , **kwargs):
    if created:
        Token.objects.create(user=instance)