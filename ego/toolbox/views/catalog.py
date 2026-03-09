from django.urls import reverse
from django.utils.translation import gettext as _


def get_tool_catalog():
    return [
        {
            "id": "todo",
            "icon": "📝",
            "featured": True,
            "category": "productivity",
            "tags": [_("效率工具"), _("待办事项"), _("任务管理")],
            "title": _("待办事项"),
            "description": _("简单高效的待办事项管理工具，帮助你组织任务和提高效率。"),
            "url": reverse("toolbox:todo"),
        },
        {
            "id": "removebg",
            "icon": "🖼️",
            "featured": True,
            "category": "productivity",
            "tags": [_("效率工具"), _("图片处理"), _("消除背景"), _("抠图")],
            "title": _("背景移除"),
            "description": _("简单高效的背景移除工具，帮助你快速移除图片中的背景。"),
            "url": reverse("toolbox:removebg"),
        },
        {
            "id": "remove_watermark",
            "icon": "💧",
            "featured": True,
            "category": "productivity",
            "tags": [_("效率工具"), _("图片处理"), _("水印移除")],
            "title": _("水印移除"),
            "description": _("简单高效的水印移除工具，帮助你快速移除图片中的水印。"),
            "url": None,
        },
        {
            "id": "excel_splitter",
            "icon": "📊",
            "featured": True,
            "category": "productivity",
            "tags": [_("效率工具"), _("数据处理"), _("Excel")],
            "title": _("Excel拆分"),
            "description": _("按指定字段拆分Excel文件，支持拆分为多个文件或多个Sheet页，打包下载。"),
            "url": reverse("toolbox:excel_splitter"),
        },
        {
            "id": "calculator",
            "icon": "🧮",
            "featured": True,
            "category": "utility",
            "tags": [_("实用工具")],
            "title": _("计算器"),
            "description": _("功能齐全的在线计算器，支持基本运算和科学计算。"),
            "url": None,
        },
        {
            "id": "notes",
            "icon": "📄",
            "featured": False,
            "category": "productivity",
            "tags": [_("效率工具")],
            "title": _("便签"),
            "description": _("快速记录灵感和想法的便签工具，支持实时保存。"),
            "url": None,
        },
        {
            "id": "timer",
            "icon": "⏱️",
            "featured": False,
            "category": "utility",
            "tags": [_("实用工具")],
            "title": _("计时器"),
            "description": _("精确的计时器和倒计时工具，适用于各种场景。"),
            "url": None,
        },
        {
            "id": "converter",
            "icon": "🔄",
            "featured": True,
            "category": "utility",
            "tags": [_("实用工具")],
            "title": _("单位转换"),
            "description": _("支持多种单位之间的转换，包括长度、重量、温度等。"),
            "url": None,
        },
        {
            "id": "password",
            "icon": "🔐",
            "featured": False,
            "category": "security",
            "tags": [_("安全工具")],
            "title": _("密码生成"),
            "description": _("安全的密码生成器，帮助你创建强密码。"),
            "url": None,
        },
    ]


def get_category_labels():
    return {
        "all": _("全部"),
        "productivity": _("效率工具"),
        "utility": _("实用工具"),
        "security": _("安全工具"),
        "dev": _("开发工具"),
    }


def get_nav_categories(tools: list[dict]):
    labels = get_category_labels()
    nav_keys = ["productivity", "utility", "security", "dev"]

    nav_groups = []
    for key in nav_keys:
        grouped = [tool for tool in tools if tool["category"] == key]
        items = [{"title": tool["title"], "url": tool["url"], "icon": tool["icon"]} for tool in grouped]
        if not items:
            items = [{"title": _("即将上线"), "url": None, "icon": "✨"}]
        nav_groups.append({"key": key, "label": labels[key], "tools": items})

    return nav_groups
