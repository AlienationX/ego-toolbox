from django.shortcuts import render
from django.utils.translation import gettext as _
from toolbox.views.catalog import get_nav_categories, get_tool_catalog
from django.http import Http404

def get_common_context():
    tools = get_tool_catalog()
    return {
        "nav_categories": get_nav_categories(tools),
    }

def about_view(request):
    context = get_common_context()
    return render(request, "toolbox/pages/about.html", context)

def privacy_view(request):
    context = get_common_context()
    return render(request, "toolbox/pages/privacy.html", context)

def terms_view(request):
    context = get_common_context()
    return render(request, "toolbox/pages/terms.html", context)

def blog_list_view(request):
    context = get_common_context()
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
    return render(request, "toolbox/pages/blog_list.html", context)

def blog_detail_view(request, post_id):
    context = get_common_context()
    context["post_id"] = post_id
    if post_id == "improve-efficiency":
        return render(request, "toolbox/pages/blog_improve_efficiency.html", context)
    elif post_id == "csv-vs-excel":
        return render(request, "toolbox/pages/blog_csv_vs_excel.html", context)
    else:
        raise Http404("Blog post not found")
