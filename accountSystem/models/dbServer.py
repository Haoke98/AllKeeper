from django.db import models
from izBasar.models import BaseModel
from .password import Password
from .server import Server


class DbServer(BaseModel):
    rootPwd = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码", null=True,
                                blank=False)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False)

    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "数据服务器"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"数据服务（{self.server.ip}）"