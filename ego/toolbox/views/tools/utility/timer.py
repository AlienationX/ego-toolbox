import logging

from django.shortcuts import render

from toolbox.views.core.context import build_tool_context

logger = logging.getLogger(__name__)


def timer_view(request):
    """计时器工具视图"""
    return render(request, "toolbox/pages/tools/utility/timer.html", build_tool_context("timer"))


ROUTES = [
    ("timer/", timer_view, "timer", "timer"),
]
