from django import forms
from django.forms import ModelForm

from ..models import BaseModel
from ..widgets import SdmPasswordInput


class UserForm(ModelForm):
    password = forms.CharField(widget=SdmPasswordInput)

    class Meta:
        model = BaseModel
        fields = []
