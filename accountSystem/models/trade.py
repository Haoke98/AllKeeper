from django.db import models

from accountSystem.models import Human
from izBasar.models import BaseModel


# Create your models here.
class CapitalAccount(BaseModel):
    name = models.CharField(verbose_name="标题", max_length=100)
    balance = models.FloatField(verbose_name="消费额度", default=0.0)
    owner = models.ForeignKey(Human, on_delete=models.CASCADE, verbose_name="拥有者", null=True, related_name='owner')

    def __str__(self):
        return f"{self.owner}---{self.name}"

    class Meta:
        verbose_name = "资金账户"
        verbose_name_plural = "所有" + verbose_name


class Transaction(BaseModel):
    _from = models.ForeignKey(related_name="_from", verbose_name="资金来源", to=CapitalAccount, on_delete=models.CASCADE)
    to = models.ForeignKey(related_name="_to", verbose_name="资金去处", to=CapitalAccount, on_delete=models.CASCADE)
    value = models.FloatField(verbose_name="金额（RMB)", default=0.0)
    at = models.DateTimeField(verbose_name="交易发生时间")
    remark = models.CharField(verbose_name="备注", max_length=50, null=True, blank=False)

    def __str__(self):
        return f"资金流动（{self.id}"

    class Meta:
        verbose_name = "资金流动"
        verbose_name_plural = "所有" + verbose_name
