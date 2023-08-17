from django.db import models


# Create your models here.
class NginxLog(models.Model):
    line = models.PositiveBigIntegerField(primary_key=True)
    ip = models.GenericIPAddressField()
    time = models.DateTimeField()
    method = models.CharField(max_length=10)
    status = models.IntegerField(verbose_name="状态码")
    pv = models.CharField(max_length=10, verbose_name="协议版本", null=True)
    bytes = models.BigIntegerField(null=True)
    tel = models.CharField(max_length=20, null=True)
    unknown = models.CharField(max_length=255, null=True)
    path = models.CharField(verbose_name="路径", max_length=255)
    query = models.CharField(max_length=255, null=True)
    userAgent = models.CharField(max_length=520, null=True)

    class Meta:
        verbose_name = "Nginx日志"
