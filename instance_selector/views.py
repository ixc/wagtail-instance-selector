import time
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.text import slugify
from instance_selector.constants import OBJECT_PK_PARAM
from instance_selector.registry import registry


def user_can_access_admin(user):
    if not user:
        return False
    return (
        user.is_superuser or user.is_staff or user.has_perm("wagtailadmin.access_admin")
    )


def instance_selector_embed(request, app_label, model_name):
    if not user_can_access_admin(request.user):
        raise PermissionDenied

    model = registry.get_model(app_label, model_name)
    instance_selector = registry.get_instance_selector(model)
    instance_selector_url = instance_selector.get_instance_selector_url()
    embed_id = slugify("%s-%s-%s" % (app_label, model_name, time.time()))
    embed_url = "%s#instance_selector_embed_id:%s" % (instance_selector_url, embed_id)

    context = {"embed_url": embed_url, "embed_id": embed_id}
    return TemplateResponse(
        request, "instance_selector/instance_selector_embed.html", context
    )


def instance_selector_lookup(request, app_label, model_name):
    if not user_can_access_admin(request.user):
        raise PermissionDenied

    object_pk = request.GET.get(OBJECT_PK_PARAM)
    if not object_pk:
        return HttpResponseBadRequest(
            "Param `%s` does have a value defined" % OBJECT_PK_PARAM
        )

    model = registry.get_model(app_label, model_name)
    instance = model.objects.get(pk=object_pk)
    instance_selector = registry.get_instance_selector(model)

    display_markup = instance_selector.get_instance_display_markup(instance)
    edit_url = instance_selector.get_instance_edit_url(instance)

    return JsonResponse(
        {"display_markup": display_markup, "edit_url": edit_url, "pk": object_pk}
    )
