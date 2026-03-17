from django.urls import path

from toolbox.views.base64_converter import base64_converter_view
from toolbox.views.csv_json_converter import csv_json_converter_view
from toolbox.views.dino_game import dino_game_view
from toolbox.views.excel_csv_converter import excel_csv_converter_view
from toolbox.views.excel_merger import excel_merger_view
from toolbox.views.excel_splitter import excel_splitter_view
from toolbox.views.feedback import feedback_view
from toolbox.views.index import index_view
from toolbox.views.json_formatter import json_formatter_view
from toolbox.views.ocr_tool import ocr_tool_view
from toolbox.views.qrcode_tool import qrcode_tool_view
from toolbox.views.removebg import removebg_view
from toolbox.views.todo import todo_view

app_name = "toolbox"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", index_view, name="index"),
    path("todo/", todo_view, name="todo"),
    path("removebg/", removebg_view, name="removebg"),
    path("dino-game/", dino_game_view, name="dino_game"),
    path("base64-converter/", base64_converter_view, name="base64_converter"),
    path("qrcode-tool/", qrcode_tool_view, name="qrcode_tool"),
    path("ocr-tool/", ocr_tool_view, name="ocr_tool"),
    path("json-formatter/", json_formatter_view, name="json_formatter"),
    path("csv-json-converter/", csv_json_converter_view, name="csv_json_converter"),
    path("excel-csv-converter/", excel_csv_converter_view, name="excel_csv_converter"),
    path("excel-merger/", excel_merger_view, name="excel_merger"),
    path("excel-splitter/", excel_splitter_view, name="excel_splitter"),
    path("feedback/", feedback_view, name="feedback"),
]
