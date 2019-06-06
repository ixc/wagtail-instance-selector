# wagtail-instance-selector

A widget for Wagtail's admin that allows you to select and create related items.

- Features and screenshots
- Installation
- Documentation
 - Using the widget as a field panel
 - Using the widget in a stream field
 - Customizing widget display
- Rationale & Credits
- Development notes

## Features

### Customizable widget display



### A consistent and feature-rich selection UI that reuses the admin's list views

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)

### Inline creation

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)


## Installation

```
pip install wagtail-instance-selector
```

and add `'instance_selector'` to `INSTALLED_APPS`.


## Documentation


### Using the widget as a field panel

```python
from django.db import models
from instance_selector.edit_handlers import InstanceSelectorPanel


class Shop(models.Model):
    pass


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    panels = [InstanceSelectorPanel("shop")]
```


#### Using the widget in a stream field

```python
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from instance_selector.blocks import InstanceSelectorBlock


class Product(models.Model):
    pass


class Service(models.Model):
    pass


class Shop(models.Model):
    content = StreamField([
        ("products", InstanceSelectorBlock(target_model="test_app.Product")),
        ("services", InstanceSelectorBlock(target_model="test_app.Service")),
    ])

    panels = [StreamFieldPanel("content")]
```

To create reusable blocks, you can subclass `InstanceSelectorBlock`.  

```python
from instance_selector.blocks import InstanceSelectorBlock


class ProductBlock(InstanceSelectorBlock):
    def __init__(self, *args, **kwargs):
        target_model = kwargs.pop("target_model", "my_app.Product")
        super(ProductBlock, self).__init__(target_model=target_model, **kwargs)
    
    class Meta:
        icon = "image"
        
# ...

StreamField([
    ("products", ProductBlock()),
])
```


### Customizing the widget for a model

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from instance_selector.registry import registry
from instance_selector.selectors import ModelAdminInstanceSelector
from .models import MyModel


@modeladmin_register
class MyModelAdmin(ModelAdmin):
    model = MyModel


class MyModelInstanceSelector(ModelAdminInstanceSelector):
    model_admin = MyModelAdmin()

    def get_instance_display_title(self, instance):
        if instance:
            return "some title"

    def get_instance_display_image_url(self, instance):
        if instance:
            return "/url/to/some/image.jpg"
            
    def get_instance_display_markup(self, instance):
        # Overriding this method allows you to completely control how the
        # widget will display the relation to this specific model
        return "<div> ... </div>"
        
    def get_instance_selector_url(self):
        # The url that the widget will render within a modal. By default, this 
        # is the ModelAdmin"s list view
        return "/url/to/some/view/"
    
    def get_instance_edit_url(self, instance):
        # The url that the user can edit the instance on. By default, this is 
        # the ModelAdmin"s edit view 
        if instance:
            return "/url/to/some/view/"


registry.register_instance_selector(MyModel, MyModelInstanceSelector())
```

Note that the `ModelAdminInstanceSelector` is designed for the common case. If your needs
are more specific, you may find some use in `instance_selector.selectors.BaseInstanceSelector`.


## Rationale & Credits

Largely, this is a rewrite of [neon-jungle/wagtailmodelchooser](https://github.com/neon-jungle/wagtailmodelchooser) 
that focuses on reusing the functionality in the admin list views. We had started a large build using 
[neon-jungle/wagtailmodelchooser](https://github.com/neon-jungle/wagtailmodelchooser) heavily, but quickly ran 
into UI problems when users needed to filter the objects or create them inline. After 
[neon-jungle/wagtailmodelchooser#11](https://github.com/neon-jungle/wagtailmodelchooser/issues/11) received little 
response, the decision was made to piece together our needs referencing parts from the ecosystem.

Much of this library was built atop of the work of others, specifically: 
- https://github.com/neon-jungle/wagtailmodelchooser
- https://github.com/springload/wagtailmodelchoosers
- https://github.com/Naeka/wagtailmodelchooser


## Development notes


### Run tests

```
pip install -r requirements.txt
python runtests.py
```


### Formatting

```
pip install -r requirements.txt
black instance_selector tests *.py
```
