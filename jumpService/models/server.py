from django.db import models
from simplepro.components import fields
from simplepro.models import BaseModel

from .net import Net, NetDevice


class Server(BaseModel):
    code = fields.CharField(verbose_name="编号", max_length=50, null=True, unique=True)
    ip = fields.CharField(verbose_name="IP地址", null=False, blank=False, help_text="可以是IPV4/IPV6", max_length=15)
    net = fields.ForeignKey(to=Net, on_delete=models.CASCADE, verbose_name="所接入的网段", null=True, blank=True)
    rootUsername = models.CharField(max_length=32, verbose_name="root用户名", blank=False, default="root")
    rootPassword = fields.PasswordInputField(max_length=32, verbose_name="root密码", blank=False, null=True)
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
    status = fields.CharField(verbose_name='状态', max_length=50, null=True, blank=True)
    bios = fields.PasswordInputField(verbose_name="BIOS", max_length=32, null=True, blank=True)
    ssh = models.IntegerField(verbose_name="SSH端口", default=22, blank=True)
    mac = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['ip', 'net'], name="server_net_ip_unique")
        ]

    def __str__(self):
        if self.code:
            if self.remark:
                return f"服务器({self.code},{self.remark})"
            else:
                return f"服务器({self.code})"
        else:
            if self.net:
                if self.remark:
                    return f"服务器({self.net.id}-{self.ip},{self.remark})"
                else:
                    return f"服务器({self.net.id}-{self.ip})"
            else:
                if self.remark:
                    return f"服务器({self.ip},{self.remark})"
                else:
                    return f"服务器({self.ip})"


class ServerNew(NetDevice):
    code = fields.CharField(verbose_name="编号", max_length=50, null=True, unique=True, blank=True)
    rootUsername = models.CharField(max_length=32, verbose_name="root用户名", blank=True, default="root")
    rootPassword = fields.PasswordInputField(max_length=32, verbose_name="root密码", blank=True, null=True)
    hosterOptions = (
        (1, '阿里云'),
        (2, '腾讯云'),
        (3, '哈密市希望科技有限公司'),
        (4, '新疆丝路融创网络科技有限公司（局域网）')
    )
    hoster = models.PositiveSmallIntegerField(choices=hosterOptions, null=True, blank=True, verbose_name="托管方")
    systemOpts = (
        ('CentOS7', 'CentOS7'),
        ('Ubuntu', 'Ubuntu'),
        ('WindowsServer2016', 'WindowsServer2016')
    )
    system = models.CharField(max_length=50, verbose_name="操作系统", default="CentOS7", choices=systemOpts, blank=True)
    bios = fields.PasswordInputField(verbose_name="BIOS", max_length=32, null=True, blank=True)
    ssh = models.IntegerField(verbose_name="SSH端口", default=22, blank=True)

    class Meta:
        verbose_name = "新的服务器模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.code:
            if self.remark:
                return f"服务器({self.code},{self.remark})"
            else:
                return f"服务器({self.code})"
        else:
            if self.remark:
                return f"服务器({self.id},{self.remark})"
            else:
                return f"服务器({self.id})"
