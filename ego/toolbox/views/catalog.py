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
            "id": "json_formatter",
            "icon": "📝",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("JSON"), _("格式化"), _("验证")],
            "title": _("JSON格式化"),
            "description": _("JSON格式化、验证和压缩工具，支持自动格式化、语法验证和折叠展开。"),
            "url": reverse("toolbox:json_formatter"),
        },
        {
            "id": "base64_converter",
            "icon": "🔢",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("Base64"), _("编码"), _("解码"), _("图片")],
            "title": _("图片Base64转换"),
            "description": _("图片的Base64编码解码工具，支持双向转换。"),
            "url": reverse("toolbox:base64_converter"),
        },
        {
            "id": "qrcode_tool",
            "icon": "📱",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("二维码"), _("生成"), _("解码")],
            "title": _("二维码工具"),
            "description": _("二维码生成与解码工具，支持文本/URL生成二维码和图片解码。"),
            "url": reverse("toolbox:qrcode_tool"),
        },
        {
            "id": "ocr_tool",
            "icon": "👁️",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("OCR"), _("图片"), _("文字提取")],
            "title": _("OCR图片文字提取"),
            "description": _("纯前端实现的OCR图片文字提取工具，支持多种语言识别。"),
            "url": reverse("toolbox:ocr_tool"),
        },
        {
            "id": "csv_json_converter",
            "icon": "📊",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("CSV"), _("JSON"), _("转换")],
            "title": _("CSV/JSON转换"),
            "description": _("CSV和JSON数据互转工具，支持自定义分隔符和表头。"),
            "url": reverse("toolbox:csv_json_converter"),
        },
        {
            "id": "excel_csv_converter",
            "icon": "📁",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("Excel"), _("CSV"), _("转换")],
            "title": _("Excel/CSV转换"),
            "description": _("Excel和CSV文件互转工具，支持上传Excel文件转换为CSV，或将CSV转换为Excel。"),
            "url": reverse("toolbox:excel_csv_converter"),
        },
        {
            "id": "excel_merger",
            "icon": "📊",
            "featured": True,
            "category": "dev",
            "tags": [_("开发工具"), _("Excel"), _("合并"), _("横向"), _("纵向")],
            "title": _("Excel文件合并"),
            "description": _("Excel文件合并工具，支持横向合并和纵向合并多个Excel文件。"),
            "url": reverse("toolbox:excel_merger"),
        },
        {
            "id": "dino_game",
            "icon": "🦖",
            "featured": True,
            "category": "game",
            "tags": [_("游戏"), _("休闲"), _("恐龙")],
            "title": _("小恐龙游戏"),
            "description": _("经典的Google小恐龙游戏，躲避仙人掌障碍物，挑战最高分！"),
            "url": reverse("toolbox:dino_game"),
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
        "game": _("游戏"),
    }


def get_nav_categories(tools: list[dict]):
    labels = get_category_labels()
    nav_keys = ["productivity", "utility", "security", "dev", "game"]

    nav_groups = []
    for key in nav_keys:
        grouped = [tool for tool in tools if tool["category"] == key]
        items = [{"title": tool["title"], "url": tool["url"], "icon": tool["icon"]} for tool in grouped]
        if not items:
            items = [{"title": _("即将上线"), "url": None, "icon": "✨"}]
        nav_groups.append({"key": key, "label": labels[key], "tools": items})

    return nav_groups
