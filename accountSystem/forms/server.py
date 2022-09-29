# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/9/29
@Software: PyCharm
@disc:
======================================="""
from django.forms import ModelForm

from accountSystem.fields import SdmPasswordField
from accountSystem.models import Server


class ServerForm(ModelForm):
    # FIXME：这里的password在InlineAdmin中也需要输入，而且是必填，但是因为实际实用不便为由暂时搁置了，需要及时处理。
    rootPassword = SdmPasswordField(label="ROOT密码", required=False, encryptByMd5=False)
    bios = SdmPasswordField(label="BIOS密码", required=False, encryptByMd5=False)

    class Meta:
        model = Server
        fields = ['group', 'hoster', 'ip', 'rootUsername', 'rootPassword', 'bios', 'ssh', 'mac', 'remark']


# class ServerUserForm(ServerFormBase):
#     password = SdmPasswordField(label="密码", required=True, encryptByMd5=False)
