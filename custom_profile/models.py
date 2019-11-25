from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=10, null=True)
    accessible_beacon_id = models.TextField(
        blank=True, null=True, default="[]")  # formatted as json array
