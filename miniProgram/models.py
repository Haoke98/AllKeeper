from django.db import models


# Create your models here.
class user(models.Model):
    openid = models.CharField(max_length=44)


class kino(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    cover = models.ImageField(upload_to='kino_cover', verbose_name='电影封面', default='kino_cover/default.png')

    def __str__(self):
        return self.name
    # episodes = models.ForeignKey(to=episode, on_delete=models.PROTECT, verbose_name='集', null=True)
    # episodes = models.ManyToOneRel(to=episode)
    # episodes = models.ManyToManyField(to=episode)


class episode(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='每一集的名字', max_length=50)
    content = models.FileField(upload_to='kino/', verbose_name='每一集的视频')
    kino = models.ForeignKey(to=kino, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
