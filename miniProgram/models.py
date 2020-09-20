from django.db import models


# Create your models here.
class user(models.Model):
    openid = models.CharField(max_length=44)


class film(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    cover = models.URLField(verbose_name='电影封面', default='kino_cover/default.png')

    def __str__(self):
        return self.name


class video(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='每一集的名字', max_length=50)
    cover = models.URLField(verbose_name='视频封面', default='kino_cover/default.png')
    url = models.URLField(verbose_name='视频链接', default="视频不见了的视频的链接")
    belongTo = models.ForeignKey(verbose_name="所属电视剧", to=film, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class settings(models.Model):
    app_name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)
    sliders = models.ManyToManyField(to=video)

    def __str__(self):
        return self.app_name
