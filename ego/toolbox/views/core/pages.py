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
        },
        {
            "id": "json-vs-xml",
            "title": _("从 XML 到 JSON：数据交换格式的演进与现代选择"),
            "date": "2024-06-05",
            "excerpt": _("回顾数据序列化的历史，深度对比 JSON 与 XML 的性能差异及其在现代 Web 开发中的地位。")
        },
        {
            "id": "uuid-deep-dive",
            "title": _("UUID 全解析：从数学原理到 v7 版本的演进"),
            "date": "2024-06-10",
            "excerpt": _("深入探讨通用唯一识别码的碰撞概率、各版本差异以及为什么 v7 是数据库主键的未来。")
        },
        {
            "id": "regex-mastery",
            "title": _("正则表达式高手之路：规避灾难性回溯"),
            "date": "2024-06-15",
            "excerpt": _("解析正则引擎的运行机制，学习如何编写高性能、安全的正则模式，避免 ReDoS 攻击。")
        },
        {
            "id": "webassembly-performance",
            "title": _("WebAssembly 如何改变浏览器端工具的性能极限"),
            "date": "2024-06-18",
            "excerpt": _("探讨 Wasm 技术如何让复杂的图像处理与数据清洗工具在浏览器中达到接近原生的运行速度。")
        },
        {
            "id": "ocr-technology",
            "title": _("从像素到文本：浏览器端 OCR 技术的现状与挑战"),
            "date": "2024-06-22",
            "excerpt": _("解析 Tesseract.js 及其背后的卷积神经网络模型如何实现无需服务器的文本识别。")
        },
        {
            "id": "local-first-privacy",
            "title": _("为什么“本地优先”是工具类产品的终极安全屏障"),
            "date": "2024-06-25",
            "excerpt": _("探讨 Privacy by Design 哲学，解释为什么在客户端处理敏感数据是构建用户信任的关键。")
        },
        {
            "id": "excel-pro-tips",
            "title": _("Excel 进阶：如何高效合并与拆分超大型工作簿"),
            "date": "2024-06-28",
            "excerpt": _("分享处理数万行数据时的合并逻辑与拆分技巧，避免因手动操作导致的数据丢失。")
        },
        {
            "id": "jwt-security",
            "title": _("现代认证基石：深入理解 JWT 与 Base64URL 编码"),
            "date": "2024-07-02",
            "excerpt": _("解析 JSON Web Token 的结构，探讨 Base64URL 在令牌传输中的必要性与安全风险。")
        },
        {
            "id": "image-compression",
            "title": _("数字图像压缩术：WebP、AVIF 与传统格式的博弈"),
            "date": "2024-07-05",
            "excerpt": _("对比不同图像格式的压缩算法，探讨如何在不损失感官质量的前提下将 Web 资源体积减半。")
        },
        {
            "id": "productivity-flow",
            "title": _("心流捍卫者：如何利用轻量化工具构建第二大脑"),
            "date": "2024-07-10",
            "excerpt": _("探讨效率工具如何通过降低认知负荷，帮助知识工作者在碎片化的任务中保持深度专注。")
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
        "json-vs-xml": "toolbox/pages/site/blog_json_xml.html",
        "uuid-deep-dive": "toolbox/pages/site/blog_uuid_math.html",
        "regex-mastery": "toolbox/pages/site/blog_regex_guide.html",
        "webassembly-performance": "toolbox/pages/site/blog_webassembly_performance.html",
        "ocr-technology": "toolbox/pages/site/blog_ocr_technology.html",
        "local-first-privacy": "toolbox/pages/site/blog_local_first.html",
        "excel-pro-tips": "toolbox/pages/site/blog_excel_pro_tips.html",
        "jwt-security": "toolbox/pages/site/blog_jwt_security.html",
        "image-compression": "toolbox/pages/site/blog_image_compression.html",
        "productivity-flow": "toolbox/pages/site/blog_productivity_flow.html",
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
