from django.forms import ModelForm

from ..fields import SdmIntegerField, SdmPasswordField
from ..models import DbService


class DbServiceForm(ModelForm):
    port = SdmIntegerField(min_value=None, max_value=None, label="端口")
    pwd = SdmPasswordField(label="root密码", encryptByMd5=False, required=False)

    class Meta:
        model = DbService
        fields = ['server', 'port', 'pwd', 'remark']
