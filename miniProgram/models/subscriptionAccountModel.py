from django.db import models

from izBasar.models import BaseModel


class SubscriptionAccount(BaseModel):
    name = models.CharField(max_length=50)
    appId = models.CharField(max_length=18)
    appSecret = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "微信订阅号"
        verbose_name_plural = verbose_name
