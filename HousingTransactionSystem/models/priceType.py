from django.db import models

from izBasar.models import BaseModel


class HousePriceType(BaseModel):
    name = models.CharField(max_length=100, verbose_name="类型名")
    unit = models.CharField(max_length=50, verbose_name="单位")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.unit)
