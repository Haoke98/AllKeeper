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

from izBasar.admin import LIST_DISPLAY
from lib import imageHelper
from lib.weiboHelper import Weibo
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
    list_display = LIST_DISPLAY + ["name", 'idCardNum', 'sex', 'birthday', 'zodiac', 'ethnic', '_tels', 'collage',
                                   'WB_ID',
                                   "weibo_avatar",
                                   'DY_ID',
                                   'DY_home',
                                   'license_plate_number', 'birthplace', 'info', '_count']
    search_fields = ['name', 'idCardNum', 'license_plate_number', 'WB_ID', 'DY_ID', 'DY_home', 'birthplace']
    list_filter = ['sex', 'birthday', 'zodiac', 'ethnic', 'collage']
    list_per_page = 14
    inlines = [TelInlineAdmin]

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
        if obj.WB_ID:
            url = f"https://weibo.com/u/{obj.WB_ID}"
            info = Weibo.info(obj.WB_ID)
            user_info = info['user']
            screen_name = user_info['screen_name']
            profile_image_url = user_info['profile_image_url']
            profile_image_base64 = imageHelper.image_to_base64(profile_image_url)
            return mark_safe(f'''
            <a href="{url}" target="blank"><img src="data:image/jpeg;base64,{profile_image_base64}" title="{screen_name}"></a>
            ''')
        else:
            return None

    weibo_avatar.short_description = "微博头像"
