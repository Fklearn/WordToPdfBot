from django.db import models

# Create your models here.


class Log(models.Model):
    user_id = models.BigIntegerField()
    state = models.JSONField()

