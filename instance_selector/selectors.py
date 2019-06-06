import inspect
from django.urls import reverse
from django.template import loader
from django.utils.safestring import mark_safe


class BaseInstanceSelector:
    def __init__(self):
        self.display_template = loader.get_template(
            self.get_instance_display_template()
        )

    def get_instance_display_markup(self, instance):
        """
        Markup representing the instance's display in a widget
        """
        markup = self.display_template.render(
            {
                "display_title": self.get_instance_display_title(instance),
                "display_image_url": self.get_instance_display_image_url(instance),
                "display_image_styles": self.get_instance_display_image_styles(
                    instance
                ),
                "edit_url": self.get_instance_edit_url(instance),
            }
        )
        return mark_safe(markup)

    def get_instance_display_title(self, instance):
        """
        A textual representation of the instance
        """
        if instance:
            return str(instance)

    def get_instance_display_image_url(self, instance):
        """
        An optional url to an image representing the instance
        """
        return None

    def get_instance_display_image_styles(self, instance):
        return {"max-width": "165px", "max-height": "165px"}

    def get_instance_display_template(self):
        return "instance_selector/instance_selector_widget_display.html"

    def get_instance_edit_url(self, instance):
        """
        The url that the instance can be edited at
        """
        raise NotImplementedError

    def get_instance_selector_url(self):
        """
        The url of a view that instances can be selected from, typically a list view
        """
        raise NotImplementedError

    def get_widget_icon(self):
        return "placeholder"


class ModelAdminInstanceSelector(BaseInstanceSelector):
    model_admin = None

    def __init__(self, model_admin=None):
        super().__init__()

        if model_admin is not None:
            self.model_admin = model_admin

        if not self.model_admin:
            raise Exception(
                "`model_admin` must be defined as an attribute on %s or passed to its __init__ method"
                % (type(self))
            )

        if inspect.isclass(self.model_admin):
            raise Exception(
                "Expected an instance of a model admin class, but received %s. "
                "You may need to instantiate your model admin before passing it to the instance selector"
                % self.model_admin
            )

    def get_instance_selector_url(self):
        index_url = self.model_admin.url_helper.index_url
        return index_url

    def get_instance_edit_url(self, instance):
        if instance:
            return self.model_admin.url_helper.get_action_url("edit", instance.pk)


class WagtailUserInstanceSelector(BaseInstanceSelector):
    def get_instance_selector_url(self):
        return reverse("wagtailusers_users:index")

    def get_instance_edit_url(self, instance):
        if instance:
            return reverse("wagtailusers_users:edit", args=[instance.pk])
