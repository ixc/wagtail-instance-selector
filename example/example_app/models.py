from django.db import models

from instance_selector.edit_handlers import InstanceSelectorPanel

from wagtail.admin.panels import FieldPanel


class Shop(models.Model):
    title = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=1000)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    image = models.ForeignKey(
        "Image",
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("title"),
        InstanceSelectorPanel("shop"),
        InstanceSelectorPanel("image"),
    ]

    def __str__(self):
        return self.title


class Image(models.Model):
    PENDING = "pending"
    APPROVED = "pending"

    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="example_app_images")
    status = models.CharField(
        max_length=1000,
        choices=((PENDING, "Pending"), (APPROVED, "Approved")),
        default=PENDING,
    )

    def __str__(self):
        return self.title
