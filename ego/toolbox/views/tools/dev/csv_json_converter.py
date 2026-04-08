import logging

from django.shortcuts import render

from toolbox.views.core.context import build_tool_context

logger = logging.getLogger(__name__)


def csv_json_converter_view(request):
    """CSV和JSON转换工具视图"""
    return render(request, "toolbox/pages/tools/dev/csv_json_converter.html", build_tool_context("csv_json_converter"))


ROUTES = [
    ("csv-json-converter/", csv_json_converter_view, "csv_json_converter", "csv_json_converter"),
]
