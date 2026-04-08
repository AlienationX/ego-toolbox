from django.shortcuts import render

from toolbox.views.core.context import build_tool_context


def base64_converter_view(request):
    """Base64转换工具视图"""
    return render(request, "toolbox/pages/tools/dev/base64_converter.html", build_tool_context("base64_converter"))


ROUTES = [
    ("base64-converter/", base64_converter_view, "base64_converter", "base64_converter"),
]
