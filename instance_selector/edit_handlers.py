from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail import VERSION as WAGTAIL_VERSION
from instance_selector.widgets import InstanceSelectorWidget


if WAGTAIL_VERSION >= (3, 0):
    if WAGTAIL_VERSION >= (4, 0):
        from wagtail.admin.panels import FieldPanel
        base_chooser_panel = FieldPanel
    else:
        from wagtail.admin.panels import BaseChooserPanel
        base_chooser_panel = BaseChooserPanel
else:
    from wagtail.admin.edit_handlers import BaseChooserPanel
    base_chooser_panel = BaseChooserPanel


class InstanceSelectorPanel(base_chooser_panel):
    model = None
    field_name = None

    def widget_overrides(self):
        # For Wagtail<3.0 we use widget_overrides
        return {self.field_name: InstanceSelectorWidget(model=self.target_model)}

    def get_form_options(self):
        # For Wagtail 3.0 we use get_form_options
        # So we can mix them to provide supports to Wagtail 2,3
        opts = super().get_form_options()
        opts["widgets"] = self.widget_overrides()
        return opts

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
