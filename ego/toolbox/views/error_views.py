from django.shortcuts import render


def bad_request(request, exception=None):
    """400错误页面视图"""
    return render(request, "toolbox/400.html", status=400)


def not_found(request, exception):
    """404错误页面视图"""
    return render(request, "toolbox/404.html", status=404)


def server_error(request):
    """500错误页面视图"""
    return render(request, "toolbox/500.html", status=500)
