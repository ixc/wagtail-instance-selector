from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import BaseChooserPanel
from instance_selector.widgets import InstanceSelectorWidget


class InstanceSelectorPanel(BaseChooserPanel):
    model = None
    field_name = None

    def widget_overrides(self):
        return {self.field_name: InstanceSelectorWidget(model=self.target_model)}

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
