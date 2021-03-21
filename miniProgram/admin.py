from django.contrib import admin

from .models import *


# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display) + ['last_changed_time']


@admin.register(Article)
class ArticleAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['description', 'cover_url', 'url']


@admin.register(RedirectUrlRelation)
class UrlRedirectorAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', '_url', 'returnValue', '_redirectUrl']

    def _redirectUrl(self, obj):
        x = mark_safe('<a href="%s">%s</a>' % (obj.redirectUrl, obj.redirectUrl))
        return x

    def _url(self, obj):
        x = mark_safe('<a href="/miniProgram/UrlRedirector%d">/miniProgram/UrlRedirector%d</a>' % (obj.id, obj.id))
        return x

    _redirectUrl.allow_tags = True


@admin.register(User)
class UserAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['last_login_time',
                                                'vip_expiredTime',
                                                "remark",
                                                'avatar', 'nickName', '_gender',
                                                'language', 'city', 'province', 'country', 'firstTimeLogin']
    date_hierarchy = 'last_login_time'

    def avatar(self, obj):
        try:
            if obj.avatarUrl == None:
                img = ''
            else:
                img = mark_safe('<img src="%s" width="50px" />' % (obj.avatarUrl,))
        except Exception as e:
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


@admin.register(Subcribtions)
class subcribtionsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['app_id', 'app_secret']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['enableVIP_mode', 'VIPprice', 'app_id', 'app_secret', 'subcribtion',
                                                'total_transaction_volume','host',
                                                ]
    list_display_links = ['__str__', 'subcribtion', 'last_changed_time']


def makeHasNotFirstAnalysed(modeladmin, request, queryset):  # 新建一个批量操作的函数，其中有三个参数：
    # 第一个参数是模型管理类，第二个request是请求，第三个queryset表示你选中的所有记录，这个函数里面会处理所有选中的queryset，所以要在操作之前用搜索或者过滤来选出需要修改的记录
    queryset.update(hasFirstAnalysed=False)  # 改变数据库表中，选中的记录的状态


makeHasNotFirstAnalysed.short_description = '让所有的Video改为没进行首次解析'  # 这个是在界面显示的描述信息


def makeHasNotAnalysed(modeladmin, request, queryset):  # 新建一个批量操作的函数，其中有三个参数：
    # 第一个参数是模型管理类，第二个request是请求，第三个queryset表示你选中的所有记录，这个函数里面会处理所有选中的queryset，所以要在操作之前用搜索或者过滤来选出需要修改的记录
    queryset.update(hasAnalysed=False)  # 改变数据库表中，选中的记录的状态


makeHasNotAnalysed.short_description = 'make all video has not been analysed.'  # 这个是在界面显示的描述信息


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    # form = VideoForm
    list_display = MyModelAdmin.list_display + ['episodeNum', 'belongTo', 'showTimes', 'id', '_cover', 'videoShow',
                                                # 'isFromSubscription', "hasFirstAnalysed", 'hasAnalysed', 'isTXV',
                                                # 'formatID', 'destinationID',
                                                # 'analysedUrl',
                                                # 'analysedUrl_ExpiredTime',
                                                # 'TXVid', 'WXVid',
                                                'vid', 'url', ]
    list_display_links = list(admin.ModelAdmin.list_display_links) + ['belongTo', '__str__']
    search_fields = ('name', 'episodeNum', 'id', 'vid'
                     # 'TXVid', 'WXVid',
                     # 'formatID', 'destinationID',
                     )
    list_filter = ['belongTo']
    list_per_page = 20

    # actions_on_bottom = [makeHasNotFirstAnalysed, ]
    # actions_on_top = [makeHasNotAnalysed, ]
    # actions = [makeHasNotAnalysed, makeHasNotFirstAnalysed]

    def videoShow(self, obj):
        try:
            if obj.cover == None:
                img = ''
            else:
                img = format_html(
                    '''<a href="{}"><video  width="200px" height="100px" onClick="copy(this,'src')" controls  name = "media" >< source  src = "{}" type = "video/mp4" ></video></a>''',
                    obj.analysedUrl, obj.analysedUrl, obj.analysedUrl)
        except Exception as e:
            img = ''
        return img

    def _cover(self, obj):
        if obj.cover == None:
            return ''
        else:
            return obj.cover.show()

    def save_model(self, request, obj, form, change):
        print("user clicked the save button just now for this video:%s change:%s" % (obj, change))
        # if change:
        obj.save()


class VideoInlineAdmin(admin.TabularInline):
    model = Video
    min_num = 0
    extra = 0
    # form = VideoForm


class ImageInlineAdmin(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(FilmType)
class FilmTypeAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['showTimes', 'id', 'name', 'unit']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', 'symbol']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', 'symbol']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    form = FilmForm
    list_display = MyModelAdmin.list_display + ['nameChinese', 'showTimes', 'id', '_cover', 'type', 'language',
                                                'country']
    list_filter = ['type', 'language', 'country']
    search_fields = list_display
    inlines = [VideoInlineAdmin]
    list_per_page = 10

    def _cover(self, obj):
        return obj.cover.show()


@admin.register(Image)
class ImageAdmin(MyModelAdmin):
    form = UploadForm
    list_display = MyModelAdmin.list_display + ['show', 'id', 'media_id', 'content']

    def show(self, obj):
        return obj.show()


@admin.register(HouseType)
class HouseTypeAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(House)
class HouseAdmin(MyModelAdmin):
    form = HouseForm
    list_display = MyModelAdmin.list_display + ['houseType', 'houseLayout', 'size', 'price', 'phoneNum', 'address',
                                                'descriptions']
    list_select_related = ['houseType', 'houseLayout']


@admin.register(HouseLayout)
class HouseLayoutAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(HousePriceType)
class HousePriceTypeAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(HousePrice)
class HousePriceAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(HouseSizeUnit)
class HouseSizeUnitAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(HouseSize)
class HouseSizeAdmin(MyModelAdmin):
    exclude = ('',)


@admin.register(StaticFiles)
class StaticFilesAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['label', 'file']
