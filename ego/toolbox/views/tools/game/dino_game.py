from django.shortcuts import render

from toolbox.views.core.context import build_tool_context


def dino_game_view(request):
    """Google小恐龙游戏视图"""
    return render(request, "toolbox/pages/tools/game/dino_game.html", build_tool_context("dino_game"))


ROUTES = [
    ("dino-game/", dino_game_view, "dino_game", "dino_game"),
]
