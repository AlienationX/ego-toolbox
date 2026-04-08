import logging

from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog

logger = logging.getLogger(__name__)


def timer_view(request):
    """计时器工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "timer"][-1]

    context = {
        "tool": tool,
        "nav_categories": get_nav_categories(all_tools),
    }
    return render(request, "toolbox/pages/timer.html", context)
