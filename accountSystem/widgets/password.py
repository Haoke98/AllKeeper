from django.forms import TextInput
from django.template import loader
from django.utils.safestring import mark_safe


class SdmPasswordInput(TextInput):
    template_name = "widgets/sdm_password_input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
