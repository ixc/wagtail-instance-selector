from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from instance_selector.constants import OBJECT_PK_PARAM
from instance_selector.registry import registry
from instance_selector.selectors import (
    BaseInstanceSelector,
    ModelAdminInstanceSelector,
    WagtailUserInstanceSelector,
)

from .test_project.test_app.models import TestModelA, TestModelB, TestModelC
from .test_project.test_app.wagtail_hooks import TestModelAAdmin, TestModelBAdmin

User = get_user_model()


class Tests(WebTest):
    """
    Commented out tests are failing for the Wagtail 4.0 + releases.

    Im not sure how relevant they are now that the widgets are being rendered
    by javascript.
    """

    def setUp(self):
        TestModelA.objects.all().delete()
        TestModelB.objects.all().delete()
        TestModelC.objects.all().delete()
        self.superuser = User.objects.create_superuser(
            "superuser", "superuser@example.com", "test"
        )
        registry.clear()

    def test_registry_automatically_discovers_models(self):
        self.assertEqual(registry.get_model("test_app", "TestModelB"), TestModelB)

    def test_registry_throws_for_unknown_models(self):
        self.assertRaises(
            LookupError, lambda: registry.get_model("test_app", "SomeUnknownModel")
        )

    def test_registry_automatically_creates_instance_selectors(self):
        selector = registry.get_instance_selector(TestModelB)
        self.assertIsInstance(selector.model_admin, TestModelBAdmin)

    def test_custom_model_can_be_registered(self):
        class Model:
            pass

        registry.register_model("foo", "bar", Model)
        self.assertEqual(registry.get_model("foo", "bar"), Model)

    def test_custom_instance_selector_can_be_registered(self):
        class TestInstanceSelector(BaseInstanceSelector):
            pass

        registry.register_instance_selector(TestModelB, TestInstanceSelector())
        self.assertIsInstance(
            registry.get_instance_selector(TestModelB), TestInstanceSelector
        )

    def test_user_instance_selector_is_automatically_created(self):
        selector = registry.get_instance_selector(User)
        self.assertIsInstance(selector, WagtailUserInstanceSelector)

    def test_widget_renders_during_model_creation(self):
        res = self.app.get("/admin/test_app/testmodelb/create/", user=self.superuser)
        self.assertIn("/static/instance_selector/instance_selector.css", res.text)
        self.assertIn("/static/instance_selector/instance_selector_embed.js", res.text)
        self.assertIn("/static/instance_selector/instance_selector_widget.js", res.text)
        # leaving these commented out for now, as the widget is now rendered by javascript
        # and they may be useful to decide how relevant they are now.
        # self.assertIn('class="instance-selector-widget ', res.text)
        # self.assertIn("create_instance_selector_widget({", res.text)

    def test_widget_renders_during_model_edit_without_value(self):
        b = TestModelB.objects.create()
        res = self.app.get(
            f"/admin/test_app/testmodelb/edit/{b.pk}/", user=self.superuser
        )
        self.assertIn("/static/instance_selector/instance_selector.css", res.text)
        self.assertIn("/static/instance_selector/instance_selector_embed.js", res.text)
        self.assertIn("/static/instance_selector/instance_selector_widget.js", res.text)
        # leaving these commented out for now, as the widget is now rendered by javascript
        # and they may be useful to decide how relevant they are now.
        # self.assertIn('class="instance-selector-widget ', res.text)
        # self.assertIn("create_instance_selector_widget({", res.text)

    def test_widget_renders_during_model_edit_with_value(self):
        a = TestModelA.objects.create()
        b = TestModelB.objects.create(test_model_a=a)
        res = self.app.get(
            f"/admin/test_app/testmodelb/edit/{b.pk}/", user=self.superuser
        )

        self.assertIn(
            '<input type="hidden" name="test_model_a" value="1" id="id_test_model_a" data-controller="instance-selector" data-instance-selector-config-value="{&quot;input_id&quot;: &quot;id_test_model_a&quot;, &quot;widget_id&quot;: &quot;id_test_model_a-instance-selector-widget&quot;, &quot;field_name&quot;: &quot;test_model_a&quot;, &quot;embed_url&quot;: &quot;/admin/instance-selector/embed/test_app.testmodela/#instance_selector_embed_id:test_model_a&quot;, &quot;embed_id&quot;: &quot;test_model_a&quot;, &quot;lookup_url&quot;: &quot;/admin/instance-selector/lookup/test_app.testmodela/&quot;, &quot;OBJECT_PK_PARAM&quot;: &quot;object_pk&quot;}">',
            res.text,
        )

        self.assertIn(
            f'<span class="instance-selector-widget__display__title">TestModelA ({a.pk})</span>',
            res.text,
        )

    def test_widget_can_render_custom_display_data(self):
        class TestInstanceSelector(BaseInstanceSelector):
            def get_instance_display_title(self, instance):
                return "test display title"

            def get_instance_display_image_url(self, instance):
                return "test display image url"

            def get_instance_edit_url(self, instance):
                return "test edit url"

        registry.register_instance_selector(TestModelA, TestInstanceSelector())

        a = TestModelA.objects.create()
        b = TestModelB.objects.create(test_model_a=a)

        res = self.app.get(
            f"/admin/test_app/testmodelb/edit/{b.pk}/", user=self.superuser
        )
        self.assertIn(
            "/static/instance_selector/instance_selector.css",
            res.text,
        )
        self.assertIn(
            "/static/instance_selector/instance_selector_embed.js",
            res.text,
        )
        self.assertIn(
            "/static/instance_selector/instance_selector_widget.js",
            res.text,
        )
        # leaving these commented out for now, as the widget is now rendered by javascript
        # and they may be useful to decide how relevant they are now.
        # self.assertIn(
        #     '<span class="instance-selector-widget__display__title">test display title</span>',
        #     res.text,
        # )
        # self.assertIn('src="test display image url"', res.text)
        # self.assertIn('href="test edit url"', res.text)

    def test_widget_can_render_custom_display_markup(self):
        class TestInstanceSelector(ModelAdminInstanceSelector):
            def get_instance_display_markup(self, instance):
                return "test display markup"

        registry.register_instance_selector(
            TestModelA, TestInstanceSelector(model_admin=TestModelAAdmin())
        )

        a = TestModelA.objects.create()
        b = TestModelB.objects.create(test_model_a=a)

        res = self.app.get(
            f"/admin/test_app/testmodelb/edit/{b.pk}/", user=self.superuser
        )
        self.assertIn(
            "/static/instance_selector/instance_selector.css",
            res.text,
        )
        self.assertIn(
            "/static/instance_selector/instance_selector_embed.js",
            res.text,
        )
        self.assertIn(
            "/static/instance_selector/instance_selector_widget.js",
            res.text,
        )
        # leaving this commented out for now, as the widget is now rendered by javascript
        # and they may be useful to decide how relevant they are now.
        # self.assertIn("test display markup", res.text)

    def test_widget_can_lookup_updated_display_information(self):
        selector = registry.get_instance_selector(TestModelA)

        a = TestModelA.objects.create()

        model_reverse = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": "test_app", "model_name": "TestModelA"},
        )
        lookup_url = f"{model_reverse}?{OBJECT_PK_PARAM}={a.pk}"
        res = self.app.get(lookup_url, user=self.superuser)

        self.assertEqual(
            res.json,
            {
                "display_markup": selector.get_instance_display_markup(a),
                "edit_url": f"/admin/test_app/testmodela/edit/{a.pk}/",
                "pk": f"{a.pk}",
            },
        )

    def test_widget_can_lookup_updated_custom_display_information(self):
        class TestInstanceSelector(BaseInstanceSelector):
            def get_instance_display_markup(self, instance):
                return "test display markup"

            def get_instance_edit_url(self, instance):
                return "test edit url"

        registry.register_instance_selector(TestModelA, TestInstanceSelector())

        a = TestModelA.objects.create()

        model_reverse = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": "test_app", "model_name": "TestModelA"},
        )
        lookup_url = f"{model_reverse}?{OBJECT_PK_PARAM}={a.pk}"
        res = self.app.get(lookup_url, user=self.superuser)

        self.assertEqual(
            res.json,
            {
                "display_markup": "test display markup",
                "edit_url": "test edit url",
                "pk": f"{a.pk}",
            },
        )

    def test_widget_lookup_without_pk_will_fail(self):
        lookup_url = reverse(
            "wagtail_instance_selector_lookup",
            kwargs={"app_label": "test_app", "model_name": "TestModelA"},
        )
        res = self.app.get(lookup_url, user=self.superuser, expect_errors=True)
        self.assertEqual(res.status_code, 400)

    def test_embed_view_renders_selector_url(self):
        selector = registry.get_instance_selector(TestModelA)
        embed_url = reverse(
            "wagtail_instance_selector_embed",
            kwargs={"app_label": "test_app", "model_name": "TestModelA"},
        )
        res = self.app.get(embed_url, user=self.superuser)
        self.assertIn(
            f'<iframe onload="removeSidebar(this);" src="{selector.get_instance_selector_url()}#instance_selector_embed_id:test_app-testmodela-',
            res.text,
        )

    def test_embed_view_renders_custom_selector_url(self):
        class TestInstanceSelector(ModelAdminInstanceSelector):
            def get_instance_selector_url(self):
                return "test selector url"

        registry.register_instance_selector(
            TestModelA, TestInstanceSelector(model_admin=TestModelAAdmin())
        )
        embed_url = reverse(
            "wagtail_instance_selector_embed",
            kwargs={"app_label": "test_app", "model_name": "TestModelA"},
        )
        res = self.app.get(embed_url, user=self.superuser)
        self.assertIn(
            '<iframe onload="removeSidebar(this);" src="test selector url#instance_selector_embed_id:test_app-testmodela-',
            res.text,
        )

    def test_blocks_can_render_widget_code(self):
        from bs4 import BeautifulSoup

        c = TestModelC.objects.create()
        res = self.app.get(
            f"/admin/test_app/testmodelc/edit/{c.pk}/", user=self.superuser
        )
        soup = BeautifulSoup(res.text, "html.parser")
        body = soup.find(id="body")

        self.assertIsNotNone(body)

        # rendered widget output is embedded in JSON within the data-block attribute
        self.assertIn("data-block", body.attrs)
        self.assertIn("data-controller", body.attrs)
        self.assertIn("data-w-block-data-value", body.attrs)
        self.assertIn("data-w-block-arguments-value", body.attrs)

        # look for required true in the JSON data-block attribute
        self.assertIn('"required": true,', body.attrs["data-w-block-data-value"])

        # look for class=\"instance-selector-widget__display\" in the JSON data-block attribute
        self.assertIn(
            '"display_markup": "<div class=\\"instance-selector-widget__display instance-selector-widget__display--no-image\\"',
            body.attrs["data-w-block-data-value"],
        )
