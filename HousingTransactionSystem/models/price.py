from django.db import models

from izBasar.models import BaseModel
from .priceType import HousePriceType


class HousePrice(BaseModel):
    priceType = models.ForeignKey(to=HousePriceType, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(verbose_name="价格（万）")

    def __str__(self):
        return "%s:%s%s" % (self.priceType.name, self.price, self.priceType.unit)
