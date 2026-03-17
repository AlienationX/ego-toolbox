import logging

from django.shortcuts import render

from .catalog import get_nav_categories, get_tool_catalog

logger = logging.getLogger(__name__)


def csv_json_converter_view(request):
    """CSV和JSON转换工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "csv_json_converter"][-1]

    context = {
        "tool": tool,
        "nav_categories": get_nav_categories(all_tools),
    }
    return render(request, "toolbox/pages/csv_json_converter.html", context)
