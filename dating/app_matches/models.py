from django.db import models

from app_user.models import CustomUser


class Match(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='like_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='like_received', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
