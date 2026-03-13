import traceback

from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _


def bad_request(request, exception=None):
    """400错误页面视图"""
    return render(request, "toolbox/400.html", status=400)


def not_found(request, exception):
    """404错误页面视图"""
    return render(request, "toolbox/404.html", status=404)


def server_error(request):
    """500错误页面视图"""
    return render(request, "toolbox/500.html", status=500)


def process_exception(request, error_details):
    # 只有HTMX请求才返回HTML错误片段
    if request.headers.get("HX-Request"):
        if settings.DEBUG:
            error_details = traceback.format_exc()
        else:
            error_details = error_details or _("服务器错误")

        context = {
            "error_title": _("服务器错误"),
            "error_message": _("系统处理您的请求时遇到了问题，请稍后重试。"),
            "error_details": error_details,
            "debug": settings.DEBUG,
        }

        return render(request, "toolbox/components/alert.html", context)
