from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

from toolbox.views.core.context import build_base_context


def about_view(request):
    return render(request, "toolbox/pages/site/about.html", build_base_context())

def privacy_view(request):
    return render(request, "toolbox/pages/site/privacy.html", build_base_context())

def terms_view(request):
    return render(request, "toolbox/pages/site/terms.html", build_base_context())

def blog_list_view(request):
    context = build_base_context()
    context["posts"] = [
        {
            "id": "improve-efficiency",
            "title": _("如何利用在线工具提升开发与工作效率"),
            "date": "2024-05-15",
            "excerpt": _("介绍如何使用 Ego Toolbox 进行高效的文本格式转换、数据清理等日常任务，从而节省大量碎片化时间。")
        },
        {
            "id": "csv-vs-excel",
            "title": _("CSV与Excel格式对比及适用场景原理解析"),
            "date": "2024-05-20",
            "excerpt": _("深入探讨 CSV 和 Excel 文件的区别、原理解析，以及为什么在程序员日常数据传输中更倾向于使用 CSV。")
        }
    ]
    return render(request, "toolbox/pages/site/blog_list.html", context)

def blog_detail_view(request, post_id):
    context = build_base_context()
    context["post_id"] = post_id
    if post_id == "improve-efficiency":
        return render(request, "toolbox/pages/site/blog_improve_efficiency.html", context)
    if post_id == "csv-vs-excel":
        return render(request, "toolbox/pages/site/blog_csv_vs_excel.html", context)
    raise Http404("Blog post not found")


ROUTES = [
    ("about/", about_view, "about"),
    ("privacy/", privacy_view, "privacy"),
    ("terms/", terms_view, "terms"),
    ("blog/", blog_list_view, "blog_list"),
    ("blog/<str:post_id>/", blog_detail_view, "blog_detail"),
]
