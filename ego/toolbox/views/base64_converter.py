from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog


def base64_converter_view(request):
    """Base64转换工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "base64_converter"][-1]

    context = {
        "tool": tool,
        "nav_categories": get_nav_categories(all_tools),
    }
    return render(request, "toolbox/pages/base64_converter.html", context)
