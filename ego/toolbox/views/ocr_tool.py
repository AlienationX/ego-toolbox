import logging
import tempfile
import os

from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog

logger = logging.getLogger(__name__)


def ocr_tool_view(request):
    """OCR图片文字提取工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "ocr_tool"][-1]

    if request.method == "GET":
        context = {
            "tool": tool,
            "nav_categories": get_nav_categories(all_tools),
        }
        return render(request, "toolbox/pages/ocr_tool.html", context)

    if request.htmx:
        action = request.POST.get("action")

        if action == "extract":
            import pytesseract
            from PIL import Image

            if not request.FILES.get("image"):
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("输入为空"), "error_message": _("请上传图片")},
                )

            image_file = request.FILES["image"]
            language = request.POST.get("language", "chi_sim")

            if not image_file:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("图片为空"), "error_message": _("图片文件为空")},
                )

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    for chunk in image_file.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name

                try:
                    image = Image.open(temp_file_path)
                    
                    text = pytesseract.image_to_string(image, lang=language)
                    
                    os.unlink(temp_file_path)
                    
                    context = {
                        "text": text.strip(),
                        "language": language,
                    }
                    return render(request, "toolbox/partials/ocr_result.html", context)

                except Exception as e:
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                    logger.error(f"OCR处理失败: {str(e)}")
                    return render(
                        request,
                        "toolbox/components/alert.html",
                        {
                            "error_title": _("OCR处理失败"),
                            "error_message": f"OCR处理失败: {str(e)}",
                        },
                    )

            except ImportError as e:
                logger.error(f"缺少必要的库: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("服务器配置错误"),
                        "error_message": "服务器缺少必要的OCR库，请联系管理员安装pytesseract和tesseract-ocr",
                    },
                )
            except Exception as e:
                logger.error(f"OCR处理错误: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("处理失败"),
                        "error_message": _("处理失败，请稍后重试"),
                    },
                )

    return render(request, "toolbox/pages/ocr_tool.html", context)
