from django.db import models
from simplepro.models import BaseModel

from .human import Human
from .marketsubject import MarketSubject


class CapitalAccountType(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=100)
    isCredit = models.BooleanField(default=False, verbose_name="信用账户", null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "资金账户类型"
        verbose_name_plural = verbose_name


# Create your models here.
class CapitalAccount(BaseModel):
    owner_natural_person = models.ForeignKey(Human, on_delete=models.CASCADE, verbose_name="拥有者(自然人)", null=True,
                                             blank=True,
                                             related_name='owner_natural_person')
    owner_market_subject = models.ForeignKey(MarketSubject, on_delete=models.CASCADE, verbose_name="拥有者(市场主题)",
                                             null=True, blank=True,
                                             related_name='owner_market_subject')
    name = models.CharField(verbose_name="账户标识", max_length=100, blank=True)
    ttype = models.ForeignKey(verbose_name="类型", to=CapitalAccountType, on_delete=models.CASCADE, null=True,
                              blank=False)
    # 信用账户属性
    fixedLimit = models.FloatField(verbose_name="固定额度", default=0.0, blank=True)
    temporaryLimit = models.FloatField(verbose_name="临时额度", default=0.0, blank=True)
    withdrawalLimit = models.FloatField(verbose_name="最高可提现", default=0.0, blank=True)
    billingDate = models.PositiveIntegerField(verbose_name="账单日", null=True, blank=True)
    repaymentDate = models.PositiveIntegerField(verbose_name="还款日", null=True, blank=True)

    def __str__(self):
        # if self.owner_natural_person:
        #     return f"{self.owner_natural_person}---{self.name}"
        # if self.owner_market_subject:
        #     return f"{self.owner_market_subject}---{self.name}"
        if self.ttype:
            if self.name:
                return f"{self.ttype.name}({self.name})"
            else:
                if self.owner_market_subject:
                    return f"{self.ttype.name}({self.owner_market_subject})"
                elif self.owner_natural_person:
                    return f"{self.ttype.name}({self.owner_natural_person})"

        else:
            return f"{self.name}"

    class Meta:
        verbose_name = "资金账户"
        verbose_name_plural = verbose_name


class Transaction(BaseModel):
    _from = models.ForeignKey(related_name="_from", verbose_name="资金来源", to=CapitalAccount, on_delete=models.CASCADE)
    to = models.ForeignKey(related_name="_to", verbose_name="资金去处", to=CapitalAccount, on_delete=models.CASCADE)
    value = models.FloatField(verbose_name="金额（RMB)", default=0.0)
    at = models.DateTimeField(verbose_name="交易发生时间")
    remark = models.CharField(verbose_name="备注", max_length=50, null=True, blank=False)

    def __str__(self):
        return f"流动资金（{self.id}"

    class Meta:
        verbose_name = "流动资金"
        verbose_name_plural = verbose_name
