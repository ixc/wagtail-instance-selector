import json

from django.forms import Media, widgets
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter

from instance_selector.constants import OBJECT_PK_PARAM
from instance_selector.registry import registry


class InstanceSelectorWidget(widgets.Input):
    # when looping over form fields, this one should appear in visible_fields, not
    # hidden_fields despite the underlying input being type="hidden"
    input_type = "hidden"
    is_hidden = False

    def __init__(self, model, **kwargs):
        self.target_model = model

        model_name = self.target_model._meta.verbose_name
        self.choose_one_text = _("Choose %s") % model_name
        self.choose_another_text = _("Choose another %s") % model_name
        self.link_to_chosen_text = _("Edit this %s") % model_name
        self.clear_choice_text = _("Clear choice")
        self.show_edit_link = True
        self.show_clear_link = True

        super().__init__(**kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # no point trying to come up with sensible semantics for when 'id' is missing
        # from attrs, so let's make sure it fails early in the process

        self.name = name
        try:
            self.id_ = attrs["id"]
        except (KeyError, TypeError) as e:
            raise TypeError(
                "InstanceSelectorWidget cannot be rendered without an 'id' attribute"
            ) from e

        value_data = self.get_value_data(value)
        widget_html = self.render_html(name, value_data, attrs)

        return mark_safe(widget_html)

    def get_value_data(self, value):
        # Given a data value (which may be None, a model instance, or a PK here),
        # extract the necessary data for rendering the widget with that value.
        # In the case of StreamField (in Wagtail >=2.13), this data will be serialised
        # via telepath https://wagtail.github.io/telepath/ to be rendered client-side,
        # which means it cannot include model instances. Instead, we return the raw
        # values used in rendering - namely: pk, display_markup and edit_url

        if not str(value).strip():  # value might be "" (Wagtail 5.0+)
            value = None

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
        value_data = value

        original_field_html = super().render(name, value_data["pk"], attrs)

        app_label = self.target_model._meta.app_label
        model_name = self.target_model._meta.model_name

        embed_url = reverse(
            "wagtail_instance_selector_embed",
            kwargs={"app_label": app_label, "model_name": model_name},
        )
        # We use the input name for the embed id so that wagtail's block code will
        # automatically replace any `__prefix__` substring with a specific id for the
        # widget instance
        embed_id = name
        embed_url += "#instance_selector_embed_id:" + embed_id

        _lookup_url = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": app_label, "model_name": model_name},
        )

        return render_to_string(
            "instance_selector/instance_selector_widget.html",
            {
                "name": name,
                "is_nonempty": value_data["pk"] is not None,
                "widget": self,
                "widget_id": f"{attrs['id']}-instance-selector-widget",
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
        # We use the input name for the embed id so that wagtail's block code will
        # automatically replace any `__prefix__` substring with a specific id for
        # the widget instance
        embed_id = name
        embed_url += "#instance_selector_embed_id:" + embed_id

        lookup_url = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": app_label, "model_name": model_name},
        )

        return {
            "input_id": id_,
            "widget_id": f"{id_}-instance-selector-widget",
            "field_name": name,
            "embed_url": embed_url,
            "embed_id": embed_id,
            "lookup_url": lookup_url,
            "OBJECT_PK_PARAM": OBJECT_PK_PARAM,
        }

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "instance-selector"
        attrs["data-instance-selector-config-value"] = json.dumps(
            self.get_js_config(self.id_, self.name)
        )
        return attrs

    @property
    def media(self):
        return Media(
            js=[
                "instance_selector/instance-selector-controller.js",
            ]
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
