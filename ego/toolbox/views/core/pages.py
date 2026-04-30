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
            "excerpt": _("探讨应对碎片化任务的最佳策略、认知负荷管理与工作流自动化。")
        },
        {
            "id": "csv-vs-excel",
            "title": _("CSV与Excel格式对比及最佳适用场景原理解析"),
            "date": "2024-05-20",
            "excerpt": _("解析其底层结构原理、性能差异以及为何需要互相转换。")
        },
        {
            "id": "base64",
            "title": _("深入浅出 Base64：前端性能优化的“双刃剑”"),
            "date": "2024-05-25",
            "excerpt": _("前端工程师与后端开发者必须理解的 Base64 编码机制与网络传输哲学。")
        },
        {
            "id": "ai-image",
            "title": _("告别套索与钢笔：AI 背景移除的工业级应用"),
            "date": "2024-05-28",
            "excerpt": _("探索基于深度学习和计算机视觉的 AI 背景移除技术如何革命性地提升效率。")
        },
        {
            "id": "qrcode",
            "title": _("剖析二维码 (QR Code)：容错、机制与信息安全"),
            "date": "2024-06-02",
            "excerpt": _("揭开 QR Code 的神秘面纱。深入探讨其定位图案机制、纠错算法与钓鱼攻击防范。")
        }
    ]
    # 按日期倒序排列
    context["posts"] = sorted(context["posts"], key=lambda x: x["date"], reverse=True)
    return render(request, "toolbox/pages/site/blog_list.html", context)

def blog_detail_view(request, post_id):
    context = build_base_context()
    context["post_id"] = post_id
    
    post_map = {
        "improve-efficiency": "toolbox/pages/site/blog_improve_efficiency.html",
        "csv-vs-excel": "toolbox/pages/site/blog_csv_vs_excel.html",
        "base64": "toolbox/pages/site/blog_base64.html",
        "ai-image": "toolbox/pages/site/blog_ai_image.html",
        "qrcode": "toolbox/pages/site/blog_qrcode.html",
    }
    
    if post_id in post_map:
        return render(request, post_map[post_id], context)
        
    raise Http404("Blog post not found")


ROUTES = [
    ("about/", about_view, "about"),
    ("privacy/", privacy_view, "privacy"),
    ("terms/", terms_view, "terms"),
    ("blog/", blog_list_view, "blog_list"),
    ("blog/<str:post_id>/", blog_detail_view, "blog_detail"),
]
