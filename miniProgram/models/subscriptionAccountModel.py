from django.db import models
from .base import MyModel


class SubscriptionAccount(MyModel):
    name = models.CharField(max_length=50)
    appId = models.CharField(max_length=18)
    appSecret = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "微信订阅号"
        verbose_name_plural = verbose_name
