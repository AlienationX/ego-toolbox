from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog


def dino_game_view(request):
    """Google小恐龙游戏视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "dino_game"][-1]

    context = {
        "tool": tool,
        "nav_categories": get_nav_categories(all_tools),
    }
    return render(request, "toolbox/pages/dino_game.html", context)
