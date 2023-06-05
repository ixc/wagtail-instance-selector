from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from instance_selector.widgets import InstanceSelectorWidget

from wagtail.admin.panels import FieldPanel


class InstanceSelectorPanel(FieldPanel):
    model = None
    field_name = None

    def get_form_options(self):
        opts = super().get_form_options()

        # Use the instance selector widget for this option
        opts["widgets"] = {self.field_name: InstanceSelectorWidget(model=self.target_model)}

        return opts

    @property
    def target_model(self):
        return self.db_field.remote_field.model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(
            render_to_string(
                self.field_template,
                {"field": self.bound_field, "instance": instance_obj},
            )
        )
