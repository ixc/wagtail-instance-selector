from django import apps


class AppConfig(apps.AppConfig):
    name = ".".join(__name__.split(".")[:-1])
    label = "instance_selector"
