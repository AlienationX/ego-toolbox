from django.shortcuts import render

from toolbox.views.core.context import build_tool_context


def qrcode_tool_view(request):
    """二维码工具视图"""
    return render(request, "toolbox/pages/tools/dev/qrcode_tool.html", build_tool_context("qrcode_tool"))


ROUTES = [
    ("qrcode-tool/", qrcode_tool_view, "qrcode_tool", "qrcode_tool"),
]
