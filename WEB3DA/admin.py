from django.contrib import admin

from miniProgram.admins.admin import MyModelAdmin
from .models import *


# 自定义表单组件 继承自URLInput 也可以不继承直接使用模板
# class ImageUrl(forms.URLInput):
#     class Media:
#         js = (
#             # 关联的js文件 存放在Django的static目录下
#             'userverifyadmin.js',
#         )
#         css = {
#             # 关联的css文件 存放在Django的static目录下
#             'all': ('userverifyadmin.css',)
#         }
#
#
# # 为需要的字段 使用自定义表单
# class VerifyForm(forms.ModelForm):
#     class Meta:
#         models = models.UserVerify
#         # fields = ['license', ]
#         widgets = {
#             # 使用自定义组件的字段
#             'license': ImageUrl(),
#         }
# from django import forms
# from miniProgram.models import Image
#
#
# class MapForm(forms.BaseModelForm):
#     base_fields = ['name', 'map']
#
#     class Meta:
#         chooseable_img_list = [(v.id, v.show()) for v in Image.objects.all()]
#         models = Map
#         widgets = {
#             'maps': forms.ChoiceField(choices=chooseable_img_list, label="贴图")
#         }
#
#     name = forms.CharField(max_length=100, min_length=0, empty_value="在这里输入贴图起名", label="贴图名称")
#

# Register your models here.
@admin.register(Map)
class MapAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['_map']

    def _map(self, obj):
        return obj.map.show()

    # form = MapForm
    # chooseable_img_list = [(v.id, v.show()) for v in Image.objects.all()]
    # formfield_overrides = {
    #
    # }

    # list_select_related = []
