from django.db import models

from izBasar.models import BaseModel


class HouseLayout(BaseModel):
    bedRoomCount = models.IntegerField(verbose_name="卧室（个数）")
    livingRoomCount = models.IntegerField(verbose_name="客厅（个数）")
    toiletCount = models.IntegerField(verbose_name="卫生间(个数)", default=1)
    courtyardCount = models.IntegerField(verbose_name="院子（个数）", default=0)

    def __str__(self):
        res = "户型："
        res += "%d室%d厅%d卫%d院" % (self.bedRoomCount, self.livingRoomCount, self.toiletCount, self.courtyardCount)
        return res
