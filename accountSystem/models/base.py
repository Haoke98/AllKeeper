from django.db import models
from simplepro.models import BaseModel


class BaseAccountModel(BaseModel):
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True