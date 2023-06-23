from django.db import models

# Create your models here.
from izBasar.models import BaseModel


class Debt(BaseModel):
    created_at = models.DateField(verbose_name="创建时间")
    ddl = models.DateField(verbose_name="还款时间")
    principle = models.FloatField(verbose_name="本金", default=0.0)
    interest = models.FloatField(verbose_name="利息/手续费", default=0.0)
    whose = models.CharField(verbose_name="所属", max_length=100)
    paid_off = models.BooleanField(verbose_name="已还清", default=False)

    class Meta:
        verbose_name = "债务"
        verbose_name_plural = "所有" + verbose_name


class Node(BaseModel):
    name = models.CharField(verbose_name="标题", max_length=100)
    balance = models.FloatField(verbose_name="消费额度", default=0.0)

    def __str__(self):
        return f"交易节点({self.name})"

    class Meta:
        verbose_name = "交易节点"
        verbose_name_plural = "所有" + verbose_name


class Transaction(BaseModel):
    _from = models.ForeignKey(related_name="_from", verbose_name="资金来源", to=Node, on_delete=models.CASCADE)
    to = models.ForeignKey(related_name="_to", verbose_name="资金去处", to=Node, on_delete=models.CASCADE)
    value = models.FloatField(verbose_name="金额（RMB)", default=0.0)
    at = models.DateField(verbose_name="交易发生时间")

    def __str__(self):
        return f"资金流动（{self.id}"

    class Meta:
        verbose_name = "资金流动"
        verbose_name_plural = "所有" + verbose_name
