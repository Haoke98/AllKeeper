from django import forms
from django.contrib import admin
from django.forms import ModelForm, TextInput
from django.template import loader
from django.utils.safestring import mark_safe

from HousingTransactionSystem.models import House
from izBasar.admin import BaseAdmin


class ImageInput(TextInput):
    separator_media_id_src = "----"
    separator_images_info = "|||||"
    template_name = "upload_multi_img/image_multi_upload.html"

    def render(self, name, value, attrs=None, renderer=None):
        print("this is render:", self, name, value, attrs, renderer)
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        context['widget']['separator_media_id_src'] = self.separator_media_id_src
        context['widget']['separator_images_info'] = self.separator_images_info
        print("this is context on it :", context)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class HouseForm(ModelForm):
    images = forms.CharField(label="@Sadam图片", widget=ImageInput, help_text="按住ctrl进行多选,最多9张", required=False)

    class Meta:
        model = House
        fields = ['houseType', 'houseLayout', 'size', 'price', 'phoneNum', 'address', 'descriptions', 'images']


@admin.register(House)
class HouseAdmin(BaseAdmin):
    form = HouseForm
    list_display = BaseAdmin.list_display + ['houseType', 'houseLayout', 'size', 'price', 'phoneNum', 'address',
                                             'descriptions']
    list_select_related = ['houseType', 'houseLayout']
