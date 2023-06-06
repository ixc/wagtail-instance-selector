from setuptools import setup

setup(
    name="wagtail-instance-selector",
    version=2.1.2,
    packages=["instance_selector"],
    include_package_data=True,
    description="A widget for Wagtail's admin that allows you to create and select related items",
    long_description="Documentation at https://github.com/ixc/wagtail-instance-selector",
    author="The Interaction Consortium",
    author_email="admins@interaction.net.au",
    url="https://github.com/ixc/wagtail-instance-selector",
    install_requires=[
        'Django',
        'wagtail',
    ],
)
