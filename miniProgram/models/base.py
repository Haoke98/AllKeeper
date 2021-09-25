from django.db import models

from accountSystem.models.base import BaseModel


class ModelWithShowRate(BaseModel):
    show_times = models.IntegerField(verbose_name="被观看次数", default=0, editable=False)

    def show(self):
        self.show_times += 1
        self.save()

    class Meta:
        abstract = True
