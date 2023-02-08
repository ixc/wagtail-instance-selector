import sys
from django.conf import settings

settings.configure(
    **{
        "DATABASES": {
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.db"}
        },
        "INSTALLED_APPS": (
            "instance_selector",
            "tests.test_project.test_app",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "wagtail.admin",
            "wagtail",
            "wagtail.contrib.modeladmin",
            "wagtail.contrib.settings",
            "wagtail.users",
            "wagtail.documents",
            "wagtail.images",
            "taggit",
        ),
        "TEMPLATES": [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                # 'APP_DIRS': True,  # Must not be set when `loaders` is defined
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                    "loaders": [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                },
            }
        ],
        "MIDDLEWARE": (
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        "STATIC_URL": "/static/",
        "ROOT_URLCONF": "tests.test_project.urls",
        "WAGTAIL_SITE_NAME": "test",
        "SECRET_KEY": "fake-key",
        "WAGTAILADMIN_BASE_URL": "http://localhost:8000",
    }
)

import django

django.setup()

from django.test.utils import get_runner

TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1, interactive=True)
failures = test_runner.run_tests(["tests"])
sys.exit(failures)
