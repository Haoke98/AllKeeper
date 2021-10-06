from django.db import models

from accountSystem.models.base import BaseModel


class Tel(BaseModel):
    content = models.CharField(max_length=11, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "手机号"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "%s" % self.content
        else:
            return "%s(%s)" % (self.content, self.remark)
