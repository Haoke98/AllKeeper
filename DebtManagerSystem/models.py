from django.db import models


# Create your models here.
class Debt(models.Model):
    created_at = models.DateField(verbose_name="创建时间")
    ddl = models.DateField(verbose_name="还款时间")
    principle = models.FloatField(verbose_name="本金")
    interest = models.FloatField(verbose_name="利息")
    whose = models.CharField(verbose_name="所属", max_length=100)
    paid_off = models.BooleanField(verbose_name="已还清", default=False)

    class Meta:
        db_table = "debt"
        verbose_name = "债务"
        verbose_name_plural = "所有" + verbose_name
