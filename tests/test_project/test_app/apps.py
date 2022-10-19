from django import apps


class AppConfig(apps.AppConfig):
    name = ".".join(__name__.split(".")[:-1])
    label = "test_app"
    default_auto_field = "django.db.models.AutoField"
