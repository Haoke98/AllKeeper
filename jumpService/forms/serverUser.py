from django.forms import ModelForm
from simplepro.components.forms import PasswordFormField

from ..models import SSHServiceUser


class ServerUserForm(ModelForm):
    pwd = PasswordFormField(label="密码", required=True, encryptByMd5=False)

    class Meta:
        model = SSHServiceUser
        fields = ['owner', 'service', 'username', 'pwd', 'group', 'f3']
