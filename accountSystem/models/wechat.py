from django.db import models
from simplepro.models import BaseModel

from .email import Email
from .human import Human
from .tel import Tel


class Wechat(BaseModel):
    id = models.CharField(verbose_name="微信号（ID）", primary_key=True, max_length=20, unique=True, null=False, blank=False,
                          db_index=True)
    nickName = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=True)
    tel = models.OneToOneField(verbose_name="绑定的手机号", to=Tel, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(verbose_name="所属账号组", to=Human, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)
    email = models.OneToOneField(verbose_name="绑定的邮箱", to=Email, on_delete=models.CASCADE, null=True, blank=True,
                                 db_index=True, help_text="你可以使用一验证过的邮箱地址登陆微信，也可以用它来找回微信密码")

    # TODO:新增绑定邮箱和QQ（创建QQ模型进行关联）

    class Meta:
        verbose_name = "微信"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "微信(%s)" % self.id
        else:
            return "微信(%s,%s)" % (self.id, self.remark)
