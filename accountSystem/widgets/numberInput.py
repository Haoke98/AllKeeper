from django.forms import NumberInput
from django.template import loader
from django.utils.safestring import mark_safe


class SdmNumberInput(NumberInput):
    template_name = "widgets/number_input.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        context.setdefault('name', "SdmNumberInput")
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
