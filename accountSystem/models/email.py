from django.db import models

from .account import BaseAccount


class Email(BaseAccount):
    # TODO: 需要增加别名了
    # TODO: 增加电子邮箱的后缀字段
    pass

    class Meta:
        verbose_name = "电子邮箱"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        A = self.username
        B = self.remark
        if A is None:
            if B is None:
                return "空邮件对象"
            else:
                return str(B)
        else:
            if B is None:
                return str(A)
            else:
                return "%s(%s)" % (A, B)
