from django.utils.functional import cached_property, lazy
from wagtail.core.blocks import ChooserBlock
from wagtail.core.utils import resolve_model_string
from instance_selector.widgets import InstanceSelectorWidget


class InstanceSelectorBlock(ChooserBlock):
    class Meta:
        icon = "placeholder"

    def __init__(self, target_model, **kwargs):
        super().__init__(**kwargs)

        self._target_model = target_model

        if self.meta.icon == "placeholder":
            # Get the icon from the chooser.
            # The chooser may not have been registered yet, depending upon
            # import orders and things, so get the icon lazily
            self.meta.icon = lazy(lambda: self.chooser.icon, str)()

    @cached_property
    def target_model(self):
        return resolve_model_string(self._target_model)

    @cached_property
    def widget(self):
        return InstanceSelectorWidget(self.target_model)

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if args:
            args = args[1:]  # Remove the args target_model

        kwargs["target_model"] = self.target_model._meta.label_lower
        return name, args, kwargs
