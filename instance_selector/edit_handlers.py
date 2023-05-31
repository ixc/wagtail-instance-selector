from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel


class InstanceSelectorPanel(FieldPanel):
    model = None
    field_name = None

    @property
    def target_model(self):
        return self.model._meta.get_field(self.field_name).remote_field.model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(
            render_to_string(
                self.field_template,
                {"field": self.bound_field, "instance": instance_obj},
            )
        )
