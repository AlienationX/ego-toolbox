def build_base_context(**extra):
    from toolbox.views.core.catalog import get_nav_categories, get_tool_catalog

    tools = get_tool_catalog()
    context = {
        "nav_categories": get_nav_categories(tools),
    }
    context.update(extra)
    return context


def build_index_context(**extra):
    from toolbox.views.core.catalog import get_category_labels

    category_labels = get_category_labels()
    context = build_base_context(
        categories=[{"key": key, "label": label} for key, label in category_labels.items()],
    )
    context.update(extra)
    return context


def build_tool_context(tool_id, **extra):
    from toolbox.views.core.catalog import get_nav_categories, get_tool_catalog

    tools = get_tool_catalog()
    tool = next(item for item in tools if item["id"] == tool_id)
    context = {
        "tool": tool,
        "nav_categories": get_nav_categories(tools),
    }
    context.update(extra)
    return context
