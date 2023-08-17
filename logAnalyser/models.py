from django.db import models


# Create your models here.
class NginxLog(models.Model):
    line = models.PositiveBigIntegerField(primary_key=True)
    ip = models.GenericIPAddressField()
    time = models.DateTimeField()
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=255)
    status = models.IntegerField()
    bytes = models.BigIntegerField(null=True)
    unknown = models.CharField(max_length=255, null=True)
    tel = models.CharField(max_length=20, null=True)
    userAgent = models.CharField(max_length=520, null=True)

    class Meta:
        verbose_name = "Nginx日志"
