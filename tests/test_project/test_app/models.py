from django.db import models
from instance_selector.edit_handlers import InstanceSelectorPanel


class TestModelA(models.Model):
    pass


class TestModelB(models.Model):
    test_model_a = models.ForeignKey(
        TestModelA, blank=True, null=True, on_delete=models.CASCADE
    )

    panels = [InstanceSelectorPanel("test_model_a")]
