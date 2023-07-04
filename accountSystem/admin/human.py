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
                                   'DY_ID',
                                   'DY_home',
                                   'license_plate_number', 'birthplace', 'info', '_count']
    search_fields = ['name', 'idCardNum']
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
