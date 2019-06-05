# wagtail-instance-selector

- Features
- Installation
- Documentation
- History
- Development notes


## Features


### Customizable widget display


### Reuses admin list view functionality


### Inline instance creation


### Nested modals..?


## Installation

```
pip install wagtail-instance-selector
```

and add `'instance_selector'` to `INSTALLED_APPS`.


## Documentation


### Basic usage


### Customizing widget display


## History 

A large CMS build started out using [neon-jungle/wagtailmodelchooser](https://github.com/neon-jungle/wagtailmodelchooser) 
heavily, but quickly ran into UI problems when users needed to filter the objects or create them inline. After 
[neon-jungle/wagtailmodelchooser#11](https://github.com/neon-jungle/wagtailmodelchooser/issues/11) received little 
response, the decision was made to piece together our needs referencing parts from the ecosystem.

Much of this library was built atop of the work of others, specifically: 
- https://github.com/neon-jungle/wagtailmodelchooser
- https://github.com/springload/wagtailmodelchoosers
- https://github.com/Naeka/wagtailmodelchooser


## Development notes


## Implementation details


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
