from django.utils.functional import cached_property, lazy
from wagtail.core.blocks import ChooserBlock
from wagtail.core.utils import resolve_model_string
from instance_selector.widgets import InstanceSelectorWidget
from instance_selector.registry import registry


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

    def get_instance_selector_icon(self):
        instance_selector = registry.get_instance_selector(self.target_model)
        return instance_selector.get_widget_icon()

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if args:
            args = args[1:]  # Remove the args target_model

        kwargs["target_model"] = self.target_model._meta.label_lower
        return name, args, kwargs
