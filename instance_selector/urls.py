from django.conf.urls import url
from instance_selector.views import instance_selector_embed, instance_selector_lookup


urlpatterns = [
    url(
        r"^instance-selector/embed/(?P<app_label>[\w-]+).(?P<model_name>[\w-]+)/$",
        instance_selector_embed,
        name="wagtail_instance_selector_embed",
    ),
    url(
        r"^instance-selector/lookup/(?P<app_label>[\w-]+).(?P<model_name>[\w-]+)/$",
        instance_selector_lookup,
        name="wagtail_instance_selector_lookup",
    ),
]
