from django.db import models

from izBasar.models import BaseModel


class Email(BaseModel):
    content = models.EmailField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="备注")
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)

    class Meta:
        verbose_name = "电子邮箱"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "%s" % self.content
        else:
            return "%s(%s)" % (self.content, self.remark)
