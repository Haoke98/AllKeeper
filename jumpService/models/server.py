from django.db import models
from simplepro.models import BaseModel


class Server(BaseModel):
    ip = models.GenericIPAddressField(verbose_name="IP地址", null=False, blank=False, unique=True,
                                      help_text="可以是IPV4/IPV6")
    rootUsername = models.CharField(max_length=32, verbose_name="root用户名", blank=False, default="root")
    rootPassword = models.CharField(max_length=32, verbose_name="root密码", blank=False, null=True)
    hosterOptions = (
        (1, '阿里云'),
        (2, '腾讯云'),
        (3, '哈密市希望科技有限公司'),
        (4, '新疆丝路融创网络科技有限公司（局域网）')
    )
    hoster = models.PositiveSmallIntegerField(choices=hosterOptions, null=True, blank=False, verbose_name="托管方")
    systemOpts = (
        ('CentOS7', 'CentOS7'),
        ('Ubuntu', 'Ubuntu'),
        ('WindowsServer2016', 'WindowsServer2016')
    )
    system = models.CharField(max_length=50, verbose_name="操作系统", default="CentOS7", choices=systemOpts)
    bios = models.CharField(verbose_name="BIOS", max_length=32, null=True, blank=True)
    ssh = models.IntegerField(verbose_name="SSH端口", default=22, blank=True)
    mac = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"服务器（{self.ip},{self.remark}）"


