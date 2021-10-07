from django.db import models

from izBasar.models import BaseModel
from .sizeUnit import HouseSizeUnit


class HouseSize(BaseModel):
    size = models.FloatField(verbose_name="数字大小")
    unit = models.ForeignKey(to=HouseSizeUnit, on_delete=models.CASCADE, verbose_name="单位")

    def __str__(self):
        return "%0.2f%s" % (self.size, self.unit.__str__())
