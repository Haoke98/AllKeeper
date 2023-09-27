from django.db import models

from izBasar.models import BaseModel


class Type(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="名称", default="未知类型")
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    # TODO: 把这些URL的解析信息全都改成模型参数！！！πParseResult(scheme='https', netloc='login.microsoftonline.com', path='/organizations/oauth2/v2.0/authorize', params='', query='redirect_uri=https%3A%2F%2Fportal.azure.com%2Fsignin%2Findex%2F&response_type=code%20id_token&scope=https%3A%2F%2Fmanagement.core.', fragment='')
    icon = models.ImageField(verbose_name="图标", null=True, blank=True)

    class Meta:
        verbose_name = "账号类型"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s" % self.name
