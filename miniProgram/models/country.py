from django.db import models

from .base import MyModel


class Country(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="国家")
    symbol = models.CharField(max_length=100, verbose_name="符号")

    class Meta:
        db_table = "country"

    def __str__(self):
        return "<%s,%s>" % (self.name, self.symbol)
