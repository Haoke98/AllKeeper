from django.contrib import admin
# Register your models here.
from django.utils.safestring import mark_safe

from izBasar.admin import showUrl, BaseAdmin
from miniProgram.models import *
from miniProgram.models.country import Country
from miniProgram.models.film import FilmType, Language, Film, FilmForm
from .subscriptionAccountAdmin import *

admin.site.site_title = "IzBasar工作室后天管理系统"
# 登录页导航条和首页导航条标题
admin.site.site_header = "IzBasar媒体工作室后台管理系统欢迎您"
# 主页标题
admin.site.index_title = "欢迎登陆"


@admin.register(Article)
class ArticleAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['description', 'cover_url', 'url']


@admin.register(RedirectUrlRelation)
class UrlRedirectAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['id', '_url', 'returnValue', '_redirectUrl']

    def _redirectUrl(self, obj):
        x = mark_safe('<a href="%s">%s</a>' % (obj.redirectUrl, obj.redirectUrl))
        return x

    def _url(self, obj):
        x = mark_safe('<a href="/miniProgram/UrlRedirector%d">/miniProgram/UrlRedirector%d</a>' % (obj.id, obj.id))
        return x

    _redirectUrl.allow_tags = True


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['last_login_time',
                                             'vip_expiredTime',
                                             "remark",
                                             'avatar', 'nickName', '_gender',
                                             'language', 'city', 'province', 'country', 'firstTimeLogin']
    date_hierarchy = 'last_login_time'

    def avatar(self, obj):
        try:
            if obj.avatarUrl is None:
                img = ''
            else:
                img = mark_safe('<img src="%s" width="50px" />' % (obj.avatarUrl,))
        except Exception as e:
            e.with_traceback()
            img = ''
        return img

    def _gender(self, obj):
        if obj.gender == 0:
            return "女"
        elif obj.gender == 1:
            return "男"
        else:
            return "-"

    avatar.allow_tags = True


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = BaseAdmin.list_display + ['__str__', 'enableVIP_mode', 'VIPprice', 'app_id', 'app_secret',
                                             'subcribtion',
                                             'total_transaction_volume', 'host',
                                             ]
    list_display_links = ['__str__', 'subcribtion', ]


def makeHasNotFirstAnalysed(modeladmin, request, queryset):  # 新建一个批量操作的函数，其中有三个参数：
    # 第一个参数是模型管理类，第二个request是请求，第三个queryset表示你选中的所有记录，这个函数里面会处理所有选中的queryset，所以要在操作之前用搜索或者过滤来选出需要修改的记录
    queryset.update(hasFirstAnalysed=False)  # 改变数据库表中，选中的记录的状态


makeHasNotFirstAnalysed.short_description = '让所有的Video改为没进行首次解析'  # 这个是在界面显示的描述信息


def makeHasNotAnalysed(modeladmin, request, queryset):  # 新建一个批量操作的函数，其中有三个参数：
    # 第一个参数是模型管理类，第二个request是请求，第三个queryset表示你选中的所有记录，这个函数里面会处理所有选中的queryset，所以要在操作之前用搜索或者过滤来选出需要修改的记录
    queryset.update(hasAnalysed=False)  # 改变数据库表中，选中的记录的状态


makeHasNotAnalysed.short_description = 'make all video has not been analysed.'  # 这个是在界面显示的描述信息


class VideoInlineAdmin(admin.TabularInline):
    model = Video
    min_num = 0
    extra = 0
    # form = VideoForm


class ImageInlineAdmin(admin.StackedInline):
    model = Image
    extra = 0


class PictureShowAdmin(BaseAdmin):
    def __init__(self, model, admin_site):
        self.list_display = super().list_display + ['_img']
        super().__init__(model, admin_site)

    def _img(self, obj):
        _url = ""
        if hasattr(obj, "original_url"):
            _url = obj.original_url
        if hasattr(obj, "cover"):
            if hasattr(obj.cover, "original_url"):
                _url = obj.cover.original_url
        return format_html(
            '''<img src="{}" width="200px" height="100px"  title="{}" onClick="show_big_img(this)"/>''',
            _url, "%s\n%s" %
                  (obj.__str__(), _url)

        )

    _img.short_description = "封面"

    class Media:
        js = (
            'js/jquery-3.6.0.min.js',
            'js/imageUtil.js'
        )


@admin.register(Image)
class ImageAdmin(PictureShowAdmin):
    form = UploadForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        print(super().list_display)
        self.list_display = super().list_display + ['_img', 'mediaId', 'content']
        print(self.list_display)


@admin.register(Film)
class FilmAdmin(PictureShowAdmin):
    form = FilmForm
    list_filter = ['type', 'language', 'country']
    search_fields = ['name', 'nameChinese']
    inlines = [VideoInlineAdmin]
    list_per_page = 10
    date_hierarchy = 'updatedAt'

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = super().list_display + ['name', 'nameChinese', 'showTimes', '_img', 'type',
                                                    'language',
                                                    'country']


@admin.register(Video)
class VideoAdmin(PictureShowAdmin):
    # form = VideoForm
    list_display_links = ['film', '__str__']
    search_fields = ('id', 'vid', 'url', 'film__name', 'film__nameChinese'
                     # 'TXVid', 'WXVid',
                     # 'formatID', 'destinationID',
                     )
    list_filter = ['isHot', 'film', 'episodeNum']
    list_per_page = 20
    autocomplete_fields = ['film']
    date_hierarchy = 'updatedAt'
    inlines = []

    # actions_on_bottom = [makeHasNotFirstAnalysed, ]
    # actions_on_top = [makeHasNotAnalysed, ]
    # actions = [makeHasNotAnalysed, makeHasNotFirstAnalysed]
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = super().list_display + ['__str__', 'isHot', 'episodeNum', 'film', 'showTimes',
                                                    '_img',
                                                    'videoShow',
                                                    # 'isFromSubscription', "hasFirstAnalysed", 'hasAnalysed', 'isTXV',
                                                    # 'formatID', 'destinationID',
                                                    # 'analysedUrl',
                                                    # 'analysedUrl_ExpiredTime',
                                                    # 'TXVid', 'WXVid',
                                                    'vid', '_url', ]

    def videoShow(self, obj):
        try:
            if obj.cover is None:
                img = ''
            else:
                img = format_html(
                    '''<a href="{}"><video  width="200px" height="100px" onClick="copy(this,'src')" controls  name = 
                    "media" >< source  src = "{}" type = "video/mp4" ></video></a>''',
                    obj.analysedUrl, obj.analysedUrl, obj.analysedUrl)
        except Exception as e:
            img = ''
        return img

    def _url(self, obj):
        return showUrl(obj.url)

    def save_model(self, request, obj, form, change):
        print("user clicked the save button just now for this video:%s change:%s" % (obj, change))
        # if change:
        obj.save()


@admin.register(FilmType)
class FilmTypeAdmin(admin.ModelAdmin):
    list_display = BaseAdmin.list_display + ['showTimes', 'id', 'name', 'unit']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = BaseAdmin.list_display + ['id', 'symbol']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = BaseAdmin.list_display + ['id', 'symbol']


@admin.register(StaticFiles)
class StaticFilesAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['label', 'file']
