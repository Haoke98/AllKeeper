# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/27
@Software: PyCharm
@disc:
======================================="""
from urllib.parse import urlparse

from django.contrib import admin
from django.forms import ModelForm
from simplepro.admin import LIST_DISPLAY, BaseAdmin, FieldOptions

from ..models import Platform, Account, URL


class URLForm(ModelForm):
    class Meta:
        model = URL
        fields = ['content', 'platform']


@admin.register(URL)
class URLAdmin(BaseAdmin):
    list_display = ['id', 'createdAt', 'updatedAt', 'content', 'domain', 'platform', 'deletedAt']
    list_filter = ['domain', 'platform']
    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': "80",
            'align': 'center',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'content': {
            'min_width': '300px',
            'align': 'left'
        },
        'platform': {
            'min_width': '160px',
            'align': 'center'
        },
        'domain': {
            'min_width': '180px',
            'align': 'center'
        },
    }


class URLInlineAdmin(admin.TabularInline):
    model = URL
    form = URLForm
    min_num = 0
    extra = 0


# Register your admin models here.
@admin.register(Platform)
class PlatformAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ["name", 'icon', '_urls', 'hostname', 'path', '_count']
    search_fields = ['name', 'url']
    list_per_page = 14
    inlines = [URLInlineAdmin, ]

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()

    _count.short_description = "关联账号的数量"

    # TODO: 把这个改成模型属性
    def hostname(self, obj):
        if obj.url:
            res = urlparse(obj.url)
            return res.hostname

    # TODO: 把这个动态解析改成模型属性
    def path(self, obj):
        if obj.url:
            res = urlparse(obj.url)
            return res.path

    def _urls(self, obj: Platform):
        res = ""
        if obj.urls.exists():
            _all = obj.urls.all()
            if len(_all) == 1:
                return f"""<a href="{_all[0].content}" target="_blank">入口</a>"""
            for i, url in enumerate(_all):
                res += f"""<a href="{url.content}" target="_blank">入口{i + 1}</a><br/>"""
        return res

    _urls.short_description = "入口"

    def formatter(self, obj: Platform, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "icon":
            if value:
                return '''<el-image style="width: 100px; height: 100px" src="{}" :preview-src-list="['{}']" lazy></el-image>'''.format(
                    value, value)
            else:
                if obj.urls.exists():
                    for url in obj.urls.all():
                        res = urlparse(url.content)
                        icon_url = f"{res.scheme}://{res.hostname}/favicon.ico"
                        return '''<el-image style="width: 100px; height: 100px" src="{}" :preview-src-list="['{}']" lazy></el-image>'''.format(
                            icon_url, icon_url)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'name': {
            'min_width': '300px',
            'align': 'left'
        },
        'icon': {
            'min_width': '160px',
            'align': 'center'
        },
        'url': {
            'min_width': '180px',
            'align': 'center'
        },
        '_count': {
            'min_width': '120px',
            'align': 'center'
        },
        'hostname': {
            'min_width': '200px',
            'align': 'left'
        },
        'path': {
            'min_width': '220px',
            'align': 'left'
        }
    }
