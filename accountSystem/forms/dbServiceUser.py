from django.forms import ModelForm

from ..fields import SdmPasswordField
from ..models import DbServiceUser


class DbServiceUserFormBase(ModelForm):
    # FIXME：这里的password在InlineAdmin中也需要输入，而且是必填，但是因为实际实用不便为由暂时搁置了，需要及时处理。
    password = SdmPasswordField(label="密码", required=False, encryptByMd5=False)

    class Meta:
        model = DbServiceUser
        fields = ['owner', 'server', 'username', 'password', 'hasRootPriority']


class DbServiceUserForm(DbServiceUserFormBase):
    password = SdmPasswordField(label="密码", required=True, encryptByMd5=False)
