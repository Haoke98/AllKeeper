from django.db import models
from simplepro.components import fields

from izBasar.models import BaseModel
from .human import Human


class Server(BaseModel):
    group = models.ForeignKey(verbose_name="所属个体/组织", to=Human, on_delete=models.CASCADE, null=True, blank=True)
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


class ServerUser(BaseModel):
    owner = models.ForeignKey(verbose_name="所属个体/组织", to=Human, on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False)
    userGroup = (
        (0, "root:x:0:"),
        (1, "bin:x:1:"),
        (2, "daemon:x:2:"),
        (3, "sys:x:3:"),
        (4, "adm:x:4:"),
        (5, "tty:x:5:"),
        (6, "disk:x:6:"),
        (7, "lp:x:7:"),
        (8, "mem:x:8:"),
        (9, "kmem:x:9:"),
        (10, "wheel:x:10:"),
        (11, "cdrom:x:11:"),
        (12, "mail:x:12:postfix"),
        (13, "man:x:15:"),
        (14, "dialout:x:18:"),
        (15, "floppy:x:19:"),
        (16, "games:x:20:"),
        (17, "tape:x:33:"))
    group = fields.IntegerField(verbose_name='用户组', choices=userGroup, null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)
    hasRootPriority = models.BooleanField(default=False, verbose_name="root权限", blank=True)
    # 密码输入框
    f3 = fields.CharField(verbose_name='测试字段（非必填）', placeholder='请输入密码', max_length=128, show_password=True, null=True,
                          blank=True, show_word_limit=True, slot='prepend', slot_text='密码')

    class Meta:
        verbose_name = "服务器用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.server.ip},{self.owner}）"
