from django.forms import ModelForm

from accountSystem.fields import SdmIntegerField
from ..models import DbService


class DbServiceForm(ModelForm):
    port = SdmIntegerField(min_value=None, max_value=None, label="端口")

    class Meta:
        model = DbService
        fields = ['server', 'ttype', 'port', 'pwd', 'remark']
