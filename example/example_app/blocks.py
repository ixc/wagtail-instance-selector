from instance_selector.blocks import InstanceSelectorBlock


class ProductBlock(InstanceSelectorBlock):
    def __init__(self, *args, **kwargs):
        target_model = kwargs.pop("target_model", "example_app.Product")
        super().__init__(target_model=target_model, **kwargs)

    class Meta:
        icon = "user"


class ImageBlock(InstanceSelectorBlock):
    def __init__(self, *args, **kwargs):
        target_model = kwargs.pop("target_model", "example_app.Image")
        super().__init__(target_model=target_model, **kwargs)

    class Meta:
        icon = "image"
