from django.forms import IntegerField

from ..widgets import SdmNumberInput


class SdmIntegerField(IntegerField):
    step: int = 1

    def __init__(self, widget=SdmNumberInput, step: int = 1, *args, **kwargs):
        self.step = step
        super().__init__(widget=widget, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, SdmNumberInput):
            attrs['step'] = self.step
        return attrs
