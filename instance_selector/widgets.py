from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.widgets import AdminChooser
from instance_selector.constants import OBJECT_PK_PARAM
from instance_selector.registry import registry


class InstanceSelectorWidget(AdminChooser):
    def __init__(self, model, **kwargs):
        self.target_model = model

        model_name = self.target_model._meta.verbose_name
        self.choose_one_text = _("Choose %s") % model_name
        self.choose_another_text = _("Choose another %s") % model_name
        self.link_to_chosen_text = _("Edit this %s") % model_name

        super().__init__(**kwargs)

    def render_html(self, name, value, attrs):
        original_field_html = super().render_html(name, value, attrs)

        instance, value = self.get_instance_and_id(self.target_model, value)

        app_label = self.target_model._meta.app_label
        model_name = self.target_model._meta.model_name
        model = registry.get_model(app_label, model_name)
        instance_selector = registry.get_instance_selector(model)

        embed_url = reverse(
            "wagtail_instance_selector_embed",
            kwargs={"app_label": app_label, "model_name": model_name},
        )
        # We use the input name for the embed id so that wagtail's block code will automatically
        # replace any `__prefix__` substring with a specific id for the widget instance
        embed_id = name
        embed_url += "#instance_selector_embed_id:" + embed_id

        lookup_url = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": app_label, "model_name": model_name},
        )

        display_markup = instance_selector.get_instance_display_markup(instance)
        edit_url = instance_selector.get_instance_edit_url(instance)

        return render_to_string(
            "instance_selector/instance_selector_widget.html",
            {
                "name": name,
                "value": value,
                "widget": self,
                "input_id": attrs["id"],
                "widget_id": "%s-instance-selector-widget" % attrs["id"],
                "original_field_html": original_field_html,
                "embed_url": embed_url,
                "embed_id": embed_id,
                "lookup_url": lookup_url,
                "OBJECT_PK_PARAM": OBJECT_PK_PARAM,
                "display_markup": display_markup,
                "edit_url": edit_url,
            },
        )
