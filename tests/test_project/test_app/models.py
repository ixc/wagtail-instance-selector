from django.db import models
from instance_selector.blocks import InstanceSelectorBlock
from instance_selector.edit_handlers import InstanceSelectorPanel

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField


class TestModelA(models.Model):
    pass


class TestModelB(models.Model):
    test_model_a = models.ForeignKey(
        TestModelA, blank=True, null=True, on_delete=models.CASCADE
    )

    panels = [InstanceSelectorPanel("test_model_a")]


class TestModelC(models.Model):
    body = (
        StreamField(
            [("test", InstanceSelectorBlock(target_model="test_app.TestModelA"))],
            use_json_field=True,
        )
    )

    panels = [FieldPanel("body")]
