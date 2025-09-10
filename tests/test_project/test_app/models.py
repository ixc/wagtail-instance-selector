from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from instance_selector.blocks import InstanceSelectorBlock
from instance_selector.edit_handlers import InstanceSelectorPanel


class TestModelA(models.Model):
    pass

    def __str__(self):
        return f"TestModelA ({self.pk})"


class TestModelB(models.Model):
    test_model_a = models.ForeignKey(
        TestModelA, blank=True, null=True, on_delete=models.CASCADE
    )

    panels = [InstanceSelectorPanel("test_model_a")]

    def __str__(self):
        return f"TestModelB ({self.pk})"


class TestModelC(models.Model):
    body = StreamField(
        [("test", InstanceSelectorBlock(target_model="test_app.TestModelA"))],
        use_json_field=True,
    )

    panels = [FieldPanel("body")]

    def __str__(self):
        return f"TestModelC ({self.pk})"
