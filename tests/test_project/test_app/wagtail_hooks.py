from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import TestModelA, TestModelB, TestModelC


@modeladmin_register
class TestModelAAdmin(ModelAdmin):
    model = TestModelA


@modeladmin_register
class TestModelBAdmin(ModelAdmin):
    model = TestModelB


@modeladmin_register
class TestModelCAdmin(ModelAdmin):
    model = TestModelC
