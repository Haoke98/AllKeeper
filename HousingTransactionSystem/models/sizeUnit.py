from django.db import models

from izBasar.models import BaseModel


class HouseSizeUnit(BaseModel):
    name = models.CharField(max_length=50, verbose_name="单位称呼")
    unit = models.CharField(max_length=50, verbose_name="单位符号")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.unit)
