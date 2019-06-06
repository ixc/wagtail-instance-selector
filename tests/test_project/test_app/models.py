from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from instance_selector.edit_handlers import InstanceSelectorPanel
from instance_selector.blocks import InstanceSelectorBlock


class TestModelA(models.Model):
    pass


class TestModelB(models.Model):
    test_model_a = models.ForeignKey(
        TestModelA, blank=True, null=True, on_delete=models.CASCADE
    )

    panels = [InstanceSelectorPanel("test_model_a")]


class TestModelC(models.Model):
    body = StreamField(
        [("test", InstanceSelectorBlock(target_model="test_app.TestModelA"))]
    )

    panels = [StreamFieldPanel("body")]
