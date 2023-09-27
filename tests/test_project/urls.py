from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls

from wagtail import urls as wagtail_urls


urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    # path('documents/', include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]
