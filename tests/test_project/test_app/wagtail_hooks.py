from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import TestModelA, TestModelB


@modeladmin_register
class TestModelAAdmin(ModelAdmin):
    model = TestModelA


@modeladmin_register
class TestModelBAdmin(ModelAdmin):
    model = TestModelB
