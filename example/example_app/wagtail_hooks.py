from django.utils.safestring import mark_safe
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from instance_selector.registry import registry
from instance_selector.selectors import ModelAdminInstanceSelector

from .models import Image, Product, Shop


@modeladmin_register
class ShopAdmin(ModelAdmin):
    model = Shop


@modeladmin_register
class ProductAdmin(ModelAdmin):
    model = Product


@modeladmin_register
class ImageAdmin(ModelAdmin):
    model = Image
    list_display = ("__str__", "image_preview")
    list_filter = ("status",)

    def image_preview(self, instance):
        if instance:
            image_url = instance.image.url
            return mark_safe(
                f'<img src="{image_url}" style="max-width: 165px; max-height: 165px;">'
            )
        return ""

    image_preview.short_description = "Image"


class ImageInstanceSelector(ModelAdminInstanceSelector):
    def get_instance_display_image_url(self, instance):
        if instance:
            return instance.image.url


registry.register_instance_selector(
    Image, ImageInstanceSelector(model_admin=ImageAdmin())
)
