from django.db import models


class Doorlock(models.Model):
    owner = models.ForeignKey(
        'auth.user',
        related_name='doorlock_owner',
        on_delete=models.CASCADE,
        null=False,
    )
    beacon_id = models.IntegerField(null=False, default=-1)
    push_id = models.IntegerField(null=False, default=-1)
    location_text = models.Textfield(null=False, default="")
    nickname = models.CharField(max_length=20, null=False, default="")