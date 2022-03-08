from django.forms import ModelForm

from ..fields import SdmPasswordField
from ..models import DbServiceUser


class DbServiceUserFormBase(ModelForm):
    password = SdmPasswordField(label="密码", required=False, encryptByMd5=False)

    class Meta:
        model = DbServiceUser
        fields = ['owner', 'server', 'username', 'password', 'hasRootPriority']


class DbServiceUserForm(DbServiceUserFormBase):
    password = SdmPasswordField(label="密码", required=True, encryptByMd5=False)
