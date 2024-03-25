# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/13
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from simplepro.admin import LIST_DISPLAY, FieldOptions

from ..models import Human, Account
from ..models import Tel


class TelForm(ModelForm):
    class Meta:
        model = Tel
        fields = ['content', 'remark']


class TelInlineAdmin(admin.TabularInline):
    model = Tel
    form = TelForm
    min_num = 0
    extra = 0


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["name", 'face', 'idCardNum', 'sex', 'birthday', 'zodiac', 'ethnic', '_tels',
                                   'collage',
                                   'DY_ID',
                                   'dy_home',
                                   'WB',
                                   'license_plate_number', 'birthplace', 'id_card_front', 'id_card_back', '_count']
    search_fields = ['name', 'idCardNum', 'license_plate_number', 'DY_ID', 'DY_home', 'birthplace']
    autocomplete_fields = ['WB', ]
    list_filter = ['sex', 'birthday', 'zodiac', 'ethnic', 'collage']
    list_per_page = 14
    fields = ['name', 'idCardNum', 'sex', 'ethnic', 'birthday', 'zodiac', 'birthplace', 'collage', 'WB', 'DY_home',
              'DY_ID', 'license_plate_number', 'face', 'id_card_front', 'id_card_back', 'info']
    inlines = [TelInlineAdmin]
    ordering = ('-updatedAt', '-createdAt')

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()

    _count.short_description = "所关联的账号数量"

    def _getTelItem(self, tel: Tel):
        item = '''
                        <div class="item">
                            <i class="phone square icon"></i>
                            <div class="content">
                              <a class="header">%s</a>

                            </div>
                        </div>
                ''' % tel.content
        return mark_safe(item)

    def _tels(self, obj):
        items: str = ""
        tels = Tel.objects.filter(owner=obj).all()
        for tel in tels:
            items += self._getTelItem(tel)
        finalList = '''
                <div class="ui list">
                    %s              
                </div>
        ''' % items
        return mark_safe(finalList)

    _tels.short_description = "联系方式"

    def weibo_avatar(self, obj):
        # if obj.WB_ID:
        #     url = f"https://weibo.com/u/{obj.WB_ID}"
        #     info = weiboHelper.info(obj.WB_ID)
        #     user_info = info['user']
        #     screen_name = user_info['screen_name']
        #     profile_image_url = user_info['profile_image_url']
        #     profile_image_base64 = imageHelper.image_to_base64(profile_image_url)
        #     return mark_safe(f'''
        #     <a href="{url}" target="blank"><img src="data:image/jpeg;base64,{profile_image_base64}" title="{screen_name}"></a>
        #     ''')
        # else:
        return None

    weibo_avatar.short_description = "微博头像"

    def dy_home(self, obj):
        if obj.DY_home:
            txt = "点击跳转"
            url = f"https://www.douyin.com/user/{obj.DY_home}"
            return mark_safe(f'''
            <a href="{url}" target="blank">{txt}</a>
            ''')

    dy_home.short_description = "抖音首页"

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'name': {
            'width': '200px',
            'align': 'left'
        },
        'idCardNum': {
            'width': '200px',
            'align': 'left'
        },
        'birthday': {
            'width': '110px',
            'align': 'left'
        },
        '_tels': {
            'width': '120px',
            'align': 'left'
        },
        'collage': {
            'width': '120px',
            'align': 'left'
        },

        'DY_ID': {
            'width': '120px',
            'align': 'left'
        },
        'WB': {
            'width': '120px',
            'align': 'left'
        },
        'dy_home': {
            'width': '100px',
            'align': 'center'
        },
        'license_plate_number': {
            'width': '120px',
            'align': 'left'
        },
        'birthplace': {
            'width': '400px',
            'align': 'left'
        },
        'info': {
            'width': '1000px',
            'align': 'left'
        },
        'face': {
            'width': '130px',
            'align': 'center'
        },
        'id_card_front': {
            'width': '140px',
            'align': 'center'
        },
        'id_card_back': {
            'width': '140px',
            'align': 'center'
        }
    }

    def formatter(self, obj, field_name, value):
        if field_name in ["face", "id_card_front", "id_card_back"]:
            if value:
                print(f"obj:{obj.id}, face:", value)
                src = f"/media/{value}"
                return f'''<el-image src="{src}" style="width:100px;height:100px;" :preview-src-list="['{src}',]">'''
        # 这里可以对value的值进行判断，比如日期格式化等
        return value
