from django.forms import ModelForm

from accountSystem.models import Account


class AccountForm(ModelForm):

    class Meta:
        model = Account
        fields = ['group', 'platform', 'username', 'pwd', 'tels', 'emails', 'wechat', 'info', 'name', 'url', 'types']
