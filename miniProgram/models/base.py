from django.db import models


class MyModel(models.Model):
    last_changed_time = models.DateTimeField(verbose_name='最近一次修改时间', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-last_changed_time']

    # def save(self, *args,**kwargs):
    #     self.last_changed_time =
    #     return super(MyModel,self).save(*args,**kwargs)
    # def save(self, *args, **kwargs):
    #     # self.last_changed_time =
    #     super().save(*args, **kwargs)