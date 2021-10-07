from django.db import models

from izBasar.models import BaseModel


class PhoneNumber(BaseModel):
    owner = models.CharField(max_length=100, verbose_name="电话号拥有者姓名", blank=True)
    number = models.BigIntegerField(verbose_name="联系电话", )

    def __str__(self):
        return "%d<%s>" % (self.number, self.owner)

    def json(self):
        return "TEL:%s" % (self.__str__())
