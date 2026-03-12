import json
import logging

from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog

logger = logging.getLogger(__name__)


def json_formatter_view(request):
    """JSON格式化工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "json_formatter"][-1]

    if request.method == "GET":
        context = {
            "tool": tool,
            "nav_categories": get_nav_categories(all_tools),
        }
        return render(request, "toolbox/pages/json_formatter.html", context)

    # POST 请求处理JSON格式化
    try:
        if request.htmx:
            action = request.POST.get("action")

            if action == "format":
                # 处理JSON格式化
                json_input = request.POST.get("json_input", "").strip()

                if not json_input:
                    return render(
                        request,
                        "toolbox/partials/error_partial.html",
                        {"error_title": _("输入为空"), "error_message": _("请输入JSON字符串")},
                    )

                try:
                    # 尝试解析JSON
                    parsed_json = json.loads(json_input)

                    # 格式化JSON（缩进2个空格）
                    formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                    print(formatted_json)

                    context = {
                        "formatted_json": formatted_json,
                        "is_valid": True,
                        "json_stats": {
                            "keys_count": _count_keys(parsed_json),
                            "depth": _calculate_depth(parsed_json),
                        },
                    }
                    return render(request, "toolbox/partials/json_formatter_result.html", context)

                except json.JSONDecodeError as e:
                    return render(
                        request,
                        "toolbox/partials/error_partial.html",
                        {
                            "error_title": _("JSON格式错误"),
                            "error_message": f"第{e.lineno}行，第{e.colno}列: {e.msg}",
                            "error_details": str(e),
                        },
                    )

            elif action == "minify":
                # 处理JSON压缩
                json_input = request.POST.get("json_input", "").strip()

                if not json_input:
                    return render(
                        request,
                        "toolbox/partials/error_partial.html",
                        {"error_title": _("输入为空"), "error_message": _("请输入JSON字符串")},
                    )

                try:
                    # 尝试解析JSON
                    parsed_json = json.loads(json_input)

                    # 压缩JSON（无缩进）
                    minified_json = json.dumps(parsed_json, ensure_ascii=False, separators=(",", ":"))
                    print(minified_json)

                    context = {
                        "formatted_json": minified_json,
                        "is_valid": True,
                        "is_minified": True,
                    }
                    return render(request, "toolbox/partials/json_formatter_result.html", context)

                except json.JSONDecodeError as e:
                    return render(
                        request,
                        "toolbox/partials/error_partial.html",
                        {
                            "error_title": _("JSON格式错误"),
                            "error_message": f"第{e.lineno}行，第{e.colno}列: {e.msg}",
                            "error_details": str(e),
                        },
                    )

    except Exception as e:
        logger.error(f"JSON格式化工具错误: {str(e)}")
        return render(
            request,
            "toolbox/partials/error_partial.html",
            {
                "error_title": _("处理失败"),
                "error_message": _("系统处理您的请求时遇到了问题，请稍后重试。"),
            },
        )


def _count_keys(obj):
    """递归计算JSON对象中的键数量"""
    if isinstance(obj, dict):
        count = len(obj)
        for value in obj.values():
            count += _count_keys(value)
        return count
    elif isinstance(obj, list):
        count = 0
        for item in obj:
            count += _count_keys(item)
        return count
    else:
        return 0


def _calculate_depth(obj):
    """递归计算JSON对象的深度"""
    if isinstance(obj, dict):
        if not obj:
            return 1
        return 1 + max(_calculate_depth(v) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return 1
        return 1 + max(_calculate_depth(item) for item in obj)
    else:
        return 1
