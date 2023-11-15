from django.forms import ModelForm
from simplepro.components.forms import PasswordFormField

from accountSystem.fields import SdmIntegerField
from ..models import DbService


class DbServiceForm(ModelForm):
    port = SdmIntegerField(min_value=None, max_value=None, label="端口")
    pwd = PasswordFormField(label="root密码", encryptByMd5=False, required=False)

    class Meta:
        model = DbService
        fields = ['server', 'ttype', 'port', 'pwd', 'remark']
