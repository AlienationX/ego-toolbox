from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .catalog import get_category_labels, get_nav_categories, get_tool_catalog


def index_view(request):
    """首页视图"""
    tools = get_tool_catalog()
    category_labels = get_category_labels()

    current_category = request.GET.get("category", "all")
    search_query = request.GET.get("q", "").strip()
    categories = [{"key": key, "label": label} for key, label in category_labels.items()]

    if current_category not in category_labels:
        current_category = "all"

    filtered_tools = []
    for tool in tools:
        if current_category != "all" and tool["category"] != current_category:
            continue
        if search_query:
            search = search_query.lower()
            if search not in tool["title"].lower() and search not in tool["description"].lower():
                continue
        filtered_tools.append(tool)

    if request.htmx:
        action = request.GET.get("action")
        print("xxx", action, current_category, search_query)

        # if action == "select":
        #     current_category = request.GET.get("category", "all")
        #     if current_category not in category_labels:
        #         current_category = "all"
        # elif action == "query":
        #     search_query = request.GET.get("q", "").strip()

        # return both filter form and grid; HTMX will apply out‑of‑band swaps
        filter_data = {"current_category": current_category, "search_query": search_query, "categories": categories}
        filter_html = render_to_string("toolbox/partials/index_filter.html", filter_data)
        grid_data = {"tools": filtered_tools}
        grid_html = render_to_string("toolbox/partials/index_tool_grid.html", grid_data)
        return HttpResponse(filter_html + grid_html)

    context = {
        "tools": filtered_tools,
        "categories": categories,
        "current_category": current_category,
        "search_query": search_query,
        "total_tools": len(tools),
        "total_usage": 12345,
        "nav_categories": get_nav_categories(tools),
    }

    return render(request, "toolbox/index.html", context)
