from setuptools import setup
import instance_selector


install_requires = ["wagtail>=4.1"]
testing_requires = ["django_webtest"]

setup(
    name="wagtail-instance-selector",
    version=instance_selector.__version__,
    packages=["instance_selector"],
    include_package_data=True,
    description="A widget for Wagtail's admin that allows you to create and select related items",
    long_description="Documentation at https://github.com/ixc/wagtail-instance-selector",
    author="The Interaction Consortium",
    author_email="admins@interaction.net.au",
    url="https://github.com/ixc/wagtail-instance-selector",
    install_requires=install_requires,
    extras_require={"testing": testing_requires},
    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Framework :: Django :: 3.2",
            "Framework :: Django :: 4.1",
            "Framework :: Django :: 4.2",
            "Framework :: Wagtail",
            "Framework :: Wagtail :: 4",
            "Framework :: Wagtail :: 5",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Utilities",
        ],
)
