from django.forms import TextInput
from django.template import loader
from django.utils.safestring import mark_safe


class CompanyAutoCompleteInput(TextInput):
    template_name = "widgets/company_auto_complete_input.html"

    def render(self, name, value, attrs=None, renderer=None):
        print("CompanyAutoCompleteWidget:", name, value, attrs, renderer)
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        context['name'] = "company"

        print("Context:", context)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
