from django.db import models

from izBasar.models import BaseModel
from .group import Group
from .password import Password


class Server(BaseModel):
    group = models.ForeignKey(verbose_name="所属个体/组织", to=Group, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField(null=False, blank=False, unique=True)
    rootPwd = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码", null=True,
                                blank=False)
    hosterOptions = (
        (1, '阿里云'),
        (2, '腾讯云'),
        (3, '哈密市希望科技有限公司'),
        (4, '新疆丝路融创网络科技有限公司（局域网）')
    )
    hoster = models.PositiveSmallIntegerField(choices=hosterOptions, null=True, blank=False, verbose_name="托管方")
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"服务器（{self.ip},{self.remark}）"
