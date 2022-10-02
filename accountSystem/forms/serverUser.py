from django.forms import ModelForm

from ..fields import SdmPasswordField
from ..models import ServerUser


class ServerUserForm(ModelForm):
    pwd = SdmPasswordField(label="密码", required=True, encryptByMd5=False)

    class Meta:
        model = ServerUser
        fields = ['owner', 'server', 'username', 'pwd', 'hasRootPriority']
