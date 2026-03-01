import uuid
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from PIL import Image
from rembg import remove

from .catalog import get_nav_categories, get_tool_catalog


def removebg_view(request):
    """背景移除工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "removebg"][-1]

    if request.method == "GET":
        context = {
            "tool": tool,
            "nav_categories": get_nav_categories(all_tools),
        }
        return render(request, "toolbox/removebg.html", context)

    # POST 请求处理图片上传
    try:
        if "image" not in request.FILES:
            return JsonResponse({"success": False, "error": _("请选择图片文件"), "error_type": "warning"})

        image_file = request.FILES["image"]

        # 验证文件类型
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
        if image_file.content_type not in allowed_types:
            return JsonResponse(
                {"success": False, "error": _("不支持的文件格式，请上传 JPG, PNG 或 WEBP 格式的图片"), "error_type": "error"}
            )

        # 验证文件大小 (10MB)
        if image_file.size > 10 * 1024 * 1024:
            return JsonResponse({"success": False, "error": _("文件大小不能超过 10MB"), "error_type": "warning"})

        # 生成唯一文件名
        file_ext = Path(image_file.name).suffix.lower()
        if not file_ext:
            file_ext = ".png"

        unique_id = str(uuid.uuid4())[:8]
        original_filename = f"original_{unique_id}{file_ext}"
        result_filename = f"removed_{unique_id}.png"

        # 确保媒体目录存在
        upload_dir = Path(settings.MEDIA_ROOT) / "removebg"
        upload_dir.mkdir(parents=True, exist_ok=True)

        original_path = upload_dir / original_filename
        result_path = upload_dir / result_filename

        # 保存原始图片
        with open(original_path, "wb+") as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # 尝试使用 rembg 移除背景

        # 打开图片
        input_image = Image.open(original_path)

        # 转换为 RGBA 模式（如果不是的话）
        if input_image.mode != "RGBA":
            input_image = input_image.convert("RGBA")

        # 移除背景
        output_image = remove(input_image)

        # 保存结果
        output_image.save(result_path, "PNG")

        # 构建结果 URL
        result_url = f"{settings.MEDIA_URL}removebg/{result_filename}"

        return JsonResponse(
            {"success": True, "result_url": result_url, "message": _("背景移除成功"), "message_type": "success"}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": f"{_('处理失败')}: {str(e)}", "error_type": "error"})
