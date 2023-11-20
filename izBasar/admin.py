from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

LIST_DISPLAY = ['id', 'updatedAt', 'createdAt']


class MinWidth:
    DATE_TIME = "168px"
    DURATION = "180px"
    IP_ADDRESS = "140px"
    PORT = "102px"
    USER_AGENT = "440px"
    HEADERS = "880px"
    UUID = "300px"
    EMAIL = "180px"
    MOBILE = "140px"
    PASSWORD = "140px"


def showUrl(url):
    if url:
        tag = mark_safe('''<a href="%s" target="blank" class="button" title="%s">URL</a>''' % (url, url))
    else:
        tag = "-"
    return tag


def avatar(url):
    return format_html(
        '''<img src="{}" width="200px" height="100px"  title="点击可浏览" onClick="show_big_img(this)"/>''',
        url, )


class BaseAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY
    date_hierarchy = 'updatedAt'

    def get_fields(self, request, obj=None):
        """
                Hook for specifying fields.
                """
        if self.fields:
            return self.fields
        # _get_form_for_get_fields() is implemented in subclasses.
        form = self._get_form_for_get_fields(request, obj)
        res = [*form.base_fields, *self.get_readonly_fields(request, obj)]
        if "info" in res:
            res.remove("info")
        res.append("info")
        return res

    # TODO：改成simplepro组件
    @staticmethod
    def username(value):
        return f'''<div style="display:flex;">
                            <el-input value="{value}" :disabled="false">
                                <template slot="append">
                                    <el-button style="color:white;border-radius: 0 4px 4px 0;width:40px;display: flex;justify-content: center;align-items: center;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')"></el-button>
                                </template>
                            </el-input>
                        </div>'''

    # TODO：改成simplepro组件
    @staticmethod
    def password(value):
        return f'''<div style="display:flex;">
                                        <el-input value="{value}" :disabled="false" :show-password="true" type="password">
                                            <template slot="append">
                                                <el-button style="color:white;border-radius: 0 4px 4px 0;width:40px;display: flex;justify-content: center;align-items: center;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')"></el-button>
                                            </template>
                                        </el-input>
                        </div>'''

    @staticmethod
    def shwoUrl(url: str):
        tag = mark_safe('''
                    <a class="ui circular icon red button" href="%s" target="blank">
                        <i class="linkify icon"></i>
                    </a>
            ''' % url)
        return tag

    class Media:

        def __init__(self):
            pass

        css = {
            'all': ()
        }
        js = [
            'js/jquery-3.6.0.min.js',
            'js/clipboardUtil.js',
        ]


class PictureShowAdmin(BaseAdmin):
    def __init__(self, model, admin_site):
        self.list_display = super().list_display + ['_img']
        super().__init__(model, admin_site)

    def _img(self, obj):
        _url = ""
        if hasattr(obj, "originalUrl"):
            _url = obj.originalUrl
        if hasattr(obj, "cover"):
            if hasattr(obj.cover, "originalUrl"):
                _url = obj.cover.originalUrl
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
