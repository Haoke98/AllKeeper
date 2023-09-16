from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

LIST_DISPLAY = ['id', 'updatedAt', 'createdAt']
SIMPLE_PRO = True

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

    @staticmethod
    def username(value):
        if SIMPLE_PRO:
            return f'''<div style="display:flex;">
                            <el-input value="{value}" :disabled="false">
                                <template slot="append">
                                    <el-button style="color:white;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')">
                                        复制
                                    </el-button>
                                </template>
                            </el-input>
                        </div>'''
        else:
            tag = mark_safe(
                '''<div class="ui left labeled button" tabindex="0">
                        <a class="ui basic right pointing label" style="width:10em;">
                        %s
                        </a>
                        <div class="ui vertical animated button blue" onclick="copyStr('%s')" >
                            <div class="hidden content" style="color:white;" >复制</div>
                            <div class="visible content">
                                    <i class="copy icon"></i>
                            </div>
                        </div>
                    </div>''' % (value, value))
            return tag

    @staticmethod
    def password(value):
        if SIMPLE_PRO:
            return f'''<div style="display:flex;">
                                        <el-input value="********" :disabled="false">
                                            <template slot="append">
                                                <el-button style="color:white;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')">
                                                    复制
                                                </el-button>
                                            </template>
                                        </el-input>
                        </div>'''
            # return f'''<button onclick="copyStr('{obj}')" ><a class="ui basic left pointing label"></a></button>'''
        else:
            tag = mark_safe(
                '''<div class="ui left labeled button" tabindex="0">
                        <div class="ui button">
                            <i class="eye icon"></i>
                        </div>
                        <a class="ui basic left pointing label">
                        ******
                        </a>
                        <div class="ui vertical animated button blue" onclick="copyStr('%s')" >
                            <div class="hidden content" style="color:white;" >复制</div>
                            <div class="visible content">
                                    <i class="copy icon"></i>
                            </div>
                        </div>
                    </div>''' % value)
            return tag

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
            'all': ('Semantic-UI-CSS-master/semantic.css',)
        }
        js = [
            'js/jquery-3.6.0.min.js',
            'Semantic-UI-CSS-master/semantic.js',
            'js/clipboardUtil.js',
            'bootstrap-3.4.1-dist/js/bootstrap.js',
            'kindeditor4.1.11/kindeditor-all.js',
            'kindeditor4.1.11/lang/zh-CN.js',
            'js/base-admin-model-kind-editor-config.js',
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
