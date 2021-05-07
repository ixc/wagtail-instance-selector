from django.utils.functional import cached_property, lazy
from wagtail.core.blocks import ChooserBlock
from wagtail.core.utils import resolve_model_string
from instance_selector.widgets import InstanceSelectorWidget
from instance_selector.registry import registry


try:
    from wagtail.core.telepath import register
    from wagtail.core.blocks.field_block import FieldBlockAdapter
except ImportError:  # do-nothing fallback for Wagtail <2.13

    def register(adapter, cls):
        pass

    class FieldBlockAdapter:
        pass


class InstanceSelectorBlock(ChooserBlock):
    class Meta:
        icon = "placeholder"

    def __init__(self, target_model, **kwargs):
        super().__init__(**kwargs)

        self._target_model = target_model

        if self.meta.icon == "placeholder":
            # The models/selectors may not have been registered yet, depending upon
            # import orders and things, so get the icon lazily
            self.meta.icon = lazy(self.get_instance_selector_icon, str)

    @cached_property
    def target_model(self):
        return resolve_model_string(self._target_model)

    @cached_property
    def widget(self):
        return InstanceSelectorWidget(self.target_model)

    def get_form_state(self, value):
        return self.widget.get_value_data(value)

    def get_instance_selector_icon(self):
        instance_selector = registry.get_instance_selector(self.target_model)
        return instance_selector.get_widget_icon()

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if args:
            args = args[1:]  # Remove the args target_model

        kwargs["target_model"] = self.target_model._meta.label_lower
        return name, args, kwargs


class InstanceSelectorBlockAdapter(FieldBlockAdapter):
    def js_args(self, block):
        name, widget, meta = super().js_args(block)

        # Fix up the 'icon' item in meta so that it's a string that we can serialize,
        # rather than a lazy reference
        if callable(meta["icon"]):
            meta["icon"] = meta["icon"]()

        return [name, widget, meta]


register(InstanceSelectorBlockAdapter(), InstanceSelectorBlock)
