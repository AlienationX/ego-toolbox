from django.urls import path

from toolbox.views.base64_converter import base64_converter_view
from toolbox.views.dino_game import dino_game_view
from toolbox.views.excel_splitter import excel_splitter_view
from toolbox.views.feedback import feedback_view
from toolbox.views.index import index_view
from toolbox.views.json_formatter import json_formatter_view
from toolbox.views.removebg import removebg_view
from toolbox.views.todo import todo_view

app_name = "toolbox"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", index_view, name="index"),
    path("todo/", todo_view, name="todo"),
    path("removebg/", removebg_view, name="removebg"),
    path("excel-splitter/", excel_splitter_view, name="excel_splitter"),
    path("json-formatter/", json_formatter_view, name="json_formatter"),
    path("dino-game/", dino_game_view, name="dino_game"),
    path("base64-converter/", base64_converter_view, name="base64_converter"),
    path("feedback/", feedback_view, name="feedback"),
]
