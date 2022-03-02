from django.forms import CharField

from ..widgets import SdmPasswordInput


class SdmPasswordField(CharField):
    pattern: str
    lenMin: int
    lenMax: int
    encryptByMd5: bool

    def __init__(self, widget=SdmPasswordInput, encryptByMd5: bool = True, lenMin: int = 8, lenMax: int = 16,
                 pattern: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!", *args,
                 **kwargs):
        self.pattern = pattern
        self.lenMin = lenMin
        self.lenMax = lenMax
        self.encryptByMd5 = encryptByMd5
        super().__init__(widget=widget, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, SdmPasswordInput):
            attrs['pattern'] = self.pattern
            attrs['lenMin'] = self.lenMin
            attrs['lenMax'] = self.lenMax
            attrs['encryptByMd5'] = self.encryptByMd5
        return attrs
