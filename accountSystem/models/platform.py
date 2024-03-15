from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel


class Platform(BaseModel):
    id = models.CharField(primary_key=True, max_length=48, default=pkHelper.uuid_generator, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name="名称", default="未知类型")
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    # TODO: 把这些URL的解析信息全都改成模型参数！！！πParseResult(scheme='https', netloc='login.microsoftonline.com', path='/organizations/oauth2/v2.0/authorize', params='', query='redirect_uri=https%3A%2F%2Fportal.azure.com%2Fsignin%2Findex%2F&response_type=code%20id_token&scope=https%3A%2F%2Fmanagement.core.', fragment='')
    icon = models.ImageField(verbose_name="图标", null=True, blank=True)

    class Meta:
        verbose_name = "平台/站点"
        verbose_name_plural = "所有" + verbose_name
        ordering = ['-updatedAt']

    def __str__(self):
        return "%s" % self.name


class URL(BaseModel):
    id = models.CharField(primary_key=True, max_length=48, default=pkHelper.uuid_generator, editable=False)
    content = models.URLField(unique=True)
    domain = models.CharField(verbose_name="域名", max_length=50)
    platform = fields.ForeignKey(to=Platform, on_delete=models.CASCADE, related_name="urls")
