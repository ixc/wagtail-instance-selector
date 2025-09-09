from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from instance_selector import urls


@hooks.register("register_admin_urls")
def register_instance_selector_urls():
    return urls.urlpatterns


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}"><script src="{}"></script><script src="{}"></script>',  # noqa: E501
        static("instance_selector/instance_selector.css"),
        static("instance_selector/instance_selector_embed.js"),
        static("instance_selector/instance_selector_widget.js"),
    )
