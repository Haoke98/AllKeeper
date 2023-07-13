from django.contrib import admin
from simplepro.decorators import button

from izBasar.admin import BaseAdmin
from ..models import BT


@admin.register(BT)
class BtAdmin(BaseAdmin):
    list_display = ['id', 'port', 'server', '_username', '_password', '_url', '_basicAuthUsername',
                    '_basicAuthPassword', 'updatedAt',
                    'createdAt', 'deletedAt', ]
    autocomplete_fields = ['server']
    list_filter = ['server']
    list_display_links = ['port', 'server']
    actions = ['test1', 'make_copy', 'custom_button']

    def _username(self, obj):
        # return BaseAdmin.username(obj.username)
        return '''<button onclick="copyStr('%s')">
                            <a class="ui basic right pointing label" style="width:10em;">%s</a>
                          </button>
                       ''' % (obj.username, obj.username)

    _username.short_description = "用户名"

    def _password(self, obj):
        # return BaseAdmin.password(obj.pwd)
        return f'''<button onclick="copyStr('{obj.pwd}')" ><a class="ui basic left pointing label">
                                    ******
                                    </a></button>'''

    _password.short_description = "密码"

    def _basicAuthUsername(self, obj):
        if obj.basicAuthUsername is None:
            return None
        # return BaseAdmin.username(obj.basicAuthUsername)
        return '''<button onclick="copyStr('%s')">
                    <a class="ui basic right pointing label" style="width:10em;">%s</a>
                  </button>
               ''' % (obj.basicAuthUsername, obj.basicAuthUsername)

    _basicAuthUsername.short_description = "BA用户名"

    def _basicAuthPassword(self, obj):
        if obj.basicAuthPwd is None:
            return None
        # return BaseAdmin.password(obj.basicAuthPwd)
        return f'''<button onclick="copyStr('{obj.basicAuthPwd}')" ><a class="ui basic left pointing label">
                            ******
                            </a></button>'''

    _basicAuthPassword.short_description = "BA密码"

    def _url(self, obj):
        uri = "http://"
        if obj.basicAuthUsername and obj.basicAuthPwd:
            uri += f"{obj.basicAuthUsername}:{obj.basicAuthPwd}@"
        if obj.domain:
            uri += obj.domain
        else:
            uri += obj.server.ip
        uri += f":{obj.port}"
        if obj.path:
            uri += f"/{obj.path}"

        # return BaseAdmin.shwoUrl(uri)
        return f"""<a target="_blank" href="{uri}" >点击进入</a>"""

    _url.short_description = "入口"

    def message_test(self, request, queryset):
        messages.add_message(request, messages.SUCCESS, '操作成功123123123123')
        messages.add_message(request, messages.ERROR, '操作成功123123123123')
        messages.add_message(request, messages.DEBUG, '操作成功123123123123')
        messages.add_message(request, messages.WARNING, '操作成功123123123123')
        messages.add_message(request, messages.INFO, '操作成功123123123123')

    message_test.short_description = '消息测试'

    # 设置按钮默认是否可点击，如果默认可点击，获取到的queryset将会是一个空的
    message_test.enable = True

    @button('测试按钮')
    def test1(self, request, queryset):
        return {
            'state': False,
            'msg': '用户关联的数据还没有删除！'
        }

    def custom_button(self, request, queryset):
        pass

    #
    # 显示的文本，与django admin一致
    custom_button.short_description = '测试按钮'
    # icon，参考element-ui icon与https://fontawesome.com
    custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'danger'

    # 给按钮追加自定义的颜色
    custom_button.style = 'color:black;'
    custom_button.confirm = "你好"

    def make_copy(self, request, queryset):
        pass

    make_copy.short_description = '复制员工'

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '40px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'port': {
            'width': '80px',
            'align': 'center'
        },
        'server': {
            'width': '340px',
            'align': 'left'
        },
        '_username': {
            'width': '200px',
            'align': 'left'
        },
        '_password': {
            'width': '80px',
            'align': 'center'
        },
        '_basicAuthUsername': {
            'width': '200px',
            'align': 'left'
        },

        '_basicAuthPassword': {
            'width': '80',
            'align': 'center'
        }
    }
