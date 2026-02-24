from django.shortcuts import render

from .catalog import get_category_labels, get_nav_categories, get_tool_catalog


def index_view(request):
    """首页视图"""
    tools = get_tool_catalog()
    category_labels = get_category_labels()

    current_category = request.GET.get("category", "all")
    if current_category not in category_labels:
        current_category = "all"

    search_query = request.GET.get("q", "").strip()

    filtered_tools = []
    for tool in tools:
        if current_category != "all" and tool["category"] != current_category:
            continue
        if search_query:
            search = search_query.lower()
            if search not in tool["title"].lower() and search not in tool["description"].lower():
                continue
        filtered_tools.append(tool)

    context = {
        "tools": filtered_tools,
        "categories": [
            {"key": key, "label": label} for key, label in category_labels.items()
        ],
        "current_category": current_category,
        "search_query": search_query,
        "total_tools": len(tools),
        "total_usage": 12345,
        "nav_categories": get_nav_categories(tools),
    }

    return render(request, "toolbox/index.html", context)
