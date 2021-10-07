from django.db import models

from izBasar.models import BaseModel


class Country(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="国家")
    symbol = models.CharField(max_length=100, verbose_name="符号")

    class Meta:
        verbose_name = "国家"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s(%s)" % (self.name, self.symbol)
