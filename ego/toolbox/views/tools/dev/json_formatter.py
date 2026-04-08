import logging

from django.shortcuts import render

from toolbox.views.core.context import build_tool_context

logger = logging.getLogger(__name__)


def json_formatter_view(request):
    """JSON格式化工具视图"""
    return render(request, "toolbox/pages/tools/dev/json_formatter.html", build_tool_context("json_formatter"))


ROUTES = [
    ("json-formatter/", json_formatter_view, "json_formatter", "json_formatter"),
]
