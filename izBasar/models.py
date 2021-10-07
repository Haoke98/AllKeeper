from django.db import models


class BaseModel(models.Model):
    # id = models.IntegerField(primary_key=True, null=False, auto_created=True, editable=False)
    createdAt = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name="创建时间", null=True,
                                     editable=False)
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="最近更新时间", null=True, editable=False)
    deletedAt = models.DateTimeField(verbose_name="被删除时间", null=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-updatedAt']


class ModelWithShowRate(BaseModel):
    show_times = models.IntegerField(verbose_name="被观看次数", default=0, editable=False)

    def show(self):
        self.show_times += 1
        self.save()

    class Meta:
        abstract = True
