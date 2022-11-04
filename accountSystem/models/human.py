from django.db import models

from izBasar.models import BaseModel


# Create your models here.

class Human(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知组")

    class Meta:
        verbose_name = "个体/组织"
        verbose_name_plural = "所有" + verbose_name
        db_table = "accountSystem_group"

    def __str__(self):
        return self.name
