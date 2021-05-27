import json
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.widgets import AdminChooser
from instance_selector.constants import OBJECT_PK_PARAM
from instance_selector.registry import registry

try:
    from wagtail.core.telepath import register
    from wagtail.core.widget_adapters import WidgetAdapter
except ImportError:  # do-nothing fallback for Wagtail <2.13

    def register(adapter, cls):
        pass

    class WidgetAdapter:
        pass


class InstanceSelectorWidget(AdminChooser):
    def __init__(self, model, **kwargs):
        self.target_model = model

        model_name = self.target_model._meta.verbose_name
        self.choose_one_text = _("Choose %s") % model_name
        self.choose_another_text = _("Choose another %s") % model_name
        self.link_to_chosen_text = _("Edit this %s") % model_name

        super().__init__(**kwargs)

    def get_value_data(self, value):
        # Given a data value (which may be None, a model instance, or a PK here),
        # extract the necessary data for rendering the widget with that value.
        # In the case of StreamField (in Wagtail >=2.13), this data will be serialised via
        # telepath https://wagtail.github.io/telepath/ to be rendered client-side, which means it
        # cannot include model instances. Instead, we return the raw values used in rendering -
        # namely: pk, display_markup and edit_url

        if value is None or isinstance(value, self.target_model):
            instance = value
        else:  # assume this is an instance ID
            instance = self.target_model.objects.get(pk=value)

        app_label = self.target_model._meta.app_label
        model_name = self.target_model._meta.model_name
        model = registry.get_model(app_label, model_name)
        instance_selector = registry.get_instance_selector(model)
        display_markup = instance_selector.get_instance_display_markup(instance)
        edit_url = instance_selector.get_instance_edit_url(instance)

        return {
            "pk": instance.pk if instance else None,
            "display_markup": display_markup,
            "edit_url": edit_url,
        }

    def render_html(self, name, value, attrs):
        if WAGTAIL_VERSION >= (2, 12):
            # From Wagtail 2.12, get_value_data is called as a preprocessing step in
            # WidgetWithScript before invoking render_html
            value_data = value
        else:
            value_data = self.get_value_data(value)

        original_field_html = super().render_html(name, value_data["pk"], attrs)

        app_label = self.target_model._meta.app_label
        model_name = self.target_model._meta.model_name

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

        return render_to_string(
            "instance_selector/instance_selector_widget.html",
            {
                "name": name,
                "is_nonempty": value_data["pk"] is not None,
                "widget": self,
                "widget_id": "%s-instance-selector-widget" % attrs["id"],
                "original_field_html": original_field_html,
                "display_markup": value_data["display_markup"],
                "edit_url": value_data["edit_url"],
            },
        )

    def get_js_config(self, id_, name):
        app_label = self.target_model._meta.app_label
        model_name = self.target_model._meta.model_name

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

        return {
            "input_id": id_,
            "widget_id": "%s-instance-selector-widget" % id_,
            "field_name": name,
            "embed_url": embed_url,
            "embed_id": embed_id,
            "lookup_url": lookup_url,
            "OBJECT_PK_PARAM": OBJECT_PK_PARAM,
        }

    def render_js_init(self, id_, name, value):
        config = self.get_js_config(id_, name)
        return "create_instance_selector_widget({config});".format(
            config=json.dumps(config)
        )


class InstanceSelectorAdapter(WidgetAdapter):
    js_constructor = "wagtailinstanceselector.widgets.InstanceSelector"

    def js_args(self, widget):
        return [
            widget.render_html(
                "__NAME__", widget.get_value_data(None), attrs={"id": "__ID__"}
            ),
            widget.get_js_config("__ID__", "__NAME__"),
        ]

    class Media:
        js = [
            "instance_selector/instance_selector_telepath.js",
        ]


register(InstanceSelectorAdapter(), InstanceSelectorWidget)
