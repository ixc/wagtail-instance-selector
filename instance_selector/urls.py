from django.urls import re_path
from instance_selector.views import instance_selector_embed, instance_selector_lookup


urlpatterns = [
    re_path(
        r"^instance-selector/embed/(?P<app_label>[\w-]+).(?P<model_name>[\w-]+)/$",
        instance_selector_embed,
        name="wagtail_instance_selector_embed",
    ),
    re_path(
        r"^instance-selector/lookup/(?P<app_label>[\w-]+).(?P<model_name>[\w-]+)/$",
        instance_selector_lookup,
        name="wagtail_instance_selector_lookup",
    ),
]
