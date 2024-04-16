from django.db import models

from .service import AbstractBaseServiceModel, AbstractBaseServiceUserModel


class DbService(AbstractBaseServiceModel):
    pwd = models.CharField(verbose_name="root密码", max_length=48, null=True, blank=True)
    typeOpts = (
        (0, 'MySQL'),
        (1, 'PostgreSQL')
    )
    ttype = models.IntegerField(verbose_name='数据库类型', choices=typeOpts, default=0, null=False, blank=False,
                                db_index=True)

    class Meta:
        verbose_name = "数据服务"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        ttype = ""
        for a, b in self.typeOpts:
            if self.ttype == a:
                ttype = b
        return f"{b}({self.server}:{self.port}）"


class DbServiceUser(AbstractBaseServiceUserModel):
    service = models.ForeignKey(to=DbService, on_delete=models.CASCADE, verbose_name="服务", null=True,
                                blank=False)

    class Meta:
        verbose_name = "数据库用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.service.server.ip},{self.owner}）"
