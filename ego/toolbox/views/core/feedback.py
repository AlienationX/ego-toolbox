from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from toolbox.models import Feedback
from toolbox.views.core.context import build_base_context


def feedback_view(request):
    """问题反馈页面视图"""
    if request.method == "GET":
        return render(request, "toolbox/pages/site/feedback.html", build_base_context())

    # POST 请求处理反馈提交
    try:
        feedback_type = request.POST.get("feedback_type", "other")
        tool_name = request.POST.get("tool_name", "")
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        contact = request.POST.get("contact", "").strip()

        # 验证必填字段
        if not title:
            return JsonResponse({"success": False, "error": _("请输入反馈标题")})
        if not content:
            return JsonResponse({"success": False, "error": _("请输入反馈内容")})

        # 创建反馈对象
        feedback = Feedback(
            feedback_type=feedback_type,
            tool_name=tool_name,
            title=title,
            content=content,
            contact=contact,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )

        # 处理图片上传
        for i in range(1, 6):
            image_key = f"image{i}"
            if image_key in request.FILES:
                image = request.FILES[image_key]
                # 验证图片大小（最大5MB）
                if image.size > 5 * 1024 * 1024:
                    return JsonResponse({"success": False, "error": _("图片大小不能超过5MB")})
                # 验证图片格式
                if not image.content_type.startswith("image/"):
                    return JsonResponse({"success": False, "error": _("请上传有效的图片文件")})
                setattr(feedback, image_key, image)

        feedback.save()

        return JsonResponse({"success": True, "message": _("感谢您的反馈！")})

    except Exception as e:
        return JsonResponse({"success": False, "error": f"{_('提交失败')}: {str(e)}"})


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


ROUTES = [
    ("feedback/", feedback_view, "feedback"),
]
