import inspect
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from instance_selector.selectors import (
    ModelAdminInstanceSelector,
    WagtailUserInstanceSelector,
)

from instance_selector.exceptions import ModelAdminLookupFailed

__all__ = ("Registry", "registry")


User = get_user_model()


class Registry:
    def __init__(self):
        self._models = {
            # ('app_label', 'model_name') => Model
        }
        self._selectors = {
            # Model => InstanceSelector instance
        }

    def get_model(self, app_label, model_name):
        key = (app_label, model_name)
        if key not in self._models:
            model = apps.get_model(app_label=app_label, model_name=model_name)
            self.register_model(app_label, model_name, model)
        return self._models[key]

    def get_instance_selector(self, model):
        if model not in self._selectors:
            from wagtail.admin.menu import admin_menu, settings_menu

            model_admin = self._find_model_admin_in_menu(admin_menu, model)
            if not model_admin:
                model_admin = self._find_model_admin_in_menu(settings_menu, model)

            if model_admin:
                instance_selector = ModelAdminInstanceSelector(model_admin=model_admin)
                self.register_instance_selector(model, instance_selector)
            elif model is User:
                if "wagtail.users" in settings.INSTALLED_APPS:
                    # Wagtail uses bespoke functional views for Users, so we apply a preconfigured
                    # variant at the last opportunity. This reduces setup difficulty, while preserving
                    # the ability to apply overrides downstream
                    self.register_instance_selector(
                        model, WagtailUserInstanceSelector()
                    )
            else:
                raise ModelAdminLookupFailed(
                    "Cannot find model admin for %s. You may need to register a model with wagtail's admin or "
                    "register an instance selector" % model
                )

        return self._selectors[model]

    def register_instance_selector(self, model, instance_selector):
        if model in self._selectors:
            raise Exception(
                "%s has already been registered. Cannot register %s -> %s"
                % (model, model, instance_selector)
            )

        if inspect.isclass(instance_selector):
            raise Exception(
                "Expected an instance of a class, but received %s. You may need to call your class before "
                "registering it" % instance_selector
            )

        self._selectors[model] = instance_selector

    def register_model(self, app_label, model_name, model):
        key = (app_label, model_name)
        if key in self._models:
            raise Exception(
                "%s has already been registered to %s. Cannot register %s -> %s"
                % (key, self._models[key], key, model)
            )
        self._models[key] = model

    def clear(self):
        """
        Forces the registry to re-discover all models and selectors
        """
        self._models = {}
        self._selectors = {}

    def _find_model_admin_in_menu(self, menu, model):
        for item in menu.registered_menu_items:
            if hasattr(item, "model_admin"):
                model_admin = item.model_admin
                if model_admin.model == model:
                    return model_admin
            if hasattr(item, "menu"):
                model_admin = self._find_model_admin_in_menu(item.menu, model)
                if model_admin:
                    return model_admin


registry = Registry()
