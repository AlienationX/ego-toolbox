from django.test import TestCase, override_settings
from django.urls import reverse

from toolbox.views.core.catalog import get_tool_catalog
from toolbox.views.core.routing import discover_routes, get_tool_route_name_map


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class ToolboxRoutingTests(TestCase):
    def test_discover_routes_contains_expected_named_routes(self):
        route_names = {route["name"] for route in discover_routes()}

        self.assertIn("index", route_names)
        self.assertIn("todo", route_names)
        self.assertIn("excel_splitter", route_names)
        self.assertIn("feedback", route_names)
        self.assertIn("about", route_names)

    def test_tool_route_name_map_matches_registered_tool_views(self):
        route_name_map = get_tool_route_name_map()

        self.assertEqual(route_name_map["todo"], "todo")
        self.assertEqual(route_name_map["removebg"], "removebg")
        self.assertEqual(route_name_map["excel_splitter"], "excel_splitter")
        self.assertEqual(route_name_map["timer"], "timer")

    def test_catalog_uses_route_metadata_to_build_tool_urls(self):
        catalog = {tool["id"]: tool for tool in get_tool_catalog()}

        self.assertEqual(catalog["todo"]["url"], reverse("toolbox:todo"))
        self.assertEqual(catalog["removebg"]["url"], reverse("toolbox:removebg"))
        self.assertEqual(catalog["excel_splitter"]["url"], reverse("toolbox:excel_splitter"))
        self.assertIsNone(catalog["remove_watermark"]["url"])

    def test_core_pages_and_tools_resolve_successfully(self):
        response = self.client.get(reverse("toolbox:index"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("toolbox:todo"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("toolbox:excel_splitter"))
        self.assertEqual(response.status_code, 200)
