from django import forms
from django.db import models
from django.forms import TextInput, ModelForm
from django.template import loader
from django.utils.safestring import mark_safe

from izBasar.models import BaseModel, ModelWithShowRate
from .country import Country
from .image import Image


class Language(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="语言")
    symbol = models.CharField(max_length=100, verbose_name="符号")

    class Meta:
        verbose_name = "语言"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s(%s)" % (self.name, self.symbol)


class FilmType(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="标签名", max_length=50)
    unit = models.CharField(verbose_name="单位", max_length=50)

    class Meta:
        verbose_name = "Film类别"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s(%s)" % (self.name, self.unit)


class Film(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    nameChinese = models.CharField(verbose_name="电影标题（中文）", max_length=100, blank=True, null=True)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, null=True)
    type = models.ForeignKey(to=FilmType, on_delete=models.CASCADE, default=1)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, default=1)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return self.name

    def json(self, withEpisodes):
        json_object = {'film_id': self.id, 'name': self.name, 'cover': self.cover.originalUrl}
        if withEpisodes:
            # episodes = Video.objects.filter(belongTo=self).order_by('-episodeNum', '-last_changed_time')
            episodes_list = []
            # for per_episode in episodes:
            #     episodes_list.append(per_episode.json(False))
            # json_object["episodes"] = episodes_list
        else:
            pass
        return json_object

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print("this Film :%s has been updated now. force_insert:%s force_update:%s," % (
        #     self.name, force_insert, force_update), using, update_fields)
        return super(Film, self).save(force_update=force_update, force_insert=force_insert, using=using,
                                      update_fields=update_fields)

    def show(self):
        self.type.show()
        super(Film, self).show()

    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, )


class ArticleAnalyseInput(TextInput):
    template_name = "ananlyse/article_analyse.html"

    def render(self, name, value, attrs=None, renderer=None):
        print("this is render:", self, name, value, attrs, renderer)
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        print("this is context on it :", context)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class FilmForm(ModelForm):
    article_analyse = forms.CharField(label="公众号文章解析：", widget=ArticleAnalyseInput, help_text="这是一个悬浮窗口",
                                      required=False)

    class Meta:
        model = Film
        fields = ['name', 'nameChinese', 'cover', 'type', 'language', 'country']
