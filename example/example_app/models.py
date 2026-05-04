from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from instance_selector.edit_handlers import InstanceSelectorPanel
from instance_selector.blocks import InstanceSelectorBlock

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.blocks import CharBlock, RichTextBlock

from modelcluster.fields import ParentalKey


class Shop(models.Model):
    title = models.CharField(max_length=1000)
    content = StreamField(
        [
            ("products", ProductBlock()),
            ("images", ImageBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("content"),
    ]

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


class ShopPage(Page):
    content = StreamField(
        [
            ("heading", CharBlock()),
            ("paragraph", RichTextBlock()),
            ("products", InstanceSelectorBlock(target_model="example_app.Product")),
        ]
    )

    content_panels = Page.content_panels + [
        InlinePanel("authors", label="Authors"),
        FieldPanel("content"),
    ]


class Author(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name


class ShopPageAuthor(Orderable):
    page = ParentalKey(ShopPage, related_name="authors")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="shop_pages"
    )

    panels = [
        InstanceSelectorPanel("author"),
    ]

    def __str__(self):
        return str(self.author)
