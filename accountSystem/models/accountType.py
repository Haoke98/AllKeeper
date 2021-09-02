from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知类型")

    class Meta:
        db_table = "account_type"
        verbose_name = "账号类型"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s账号" % self.name
