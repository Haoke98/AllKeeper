from django.db import models

from izBasar.models import BaseModel


# Create your models here.

class Human(BaseModel):
    name = models.CharField(max_length=50, verbose_name="姓名", default="未知组")
    idCardNum = models.CharField(max_length=50, verbose_name="身份证号", null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(("男", "男"), ("女", "女")),
                           verbose_name="性别", null=True, blank=True)

    class Meta:
        verbose_name = "个体/组织"
        verbose_name_plural = "社工库"
        db_table = "accountSystem_group"

    def __str__(self):
        return self.name
