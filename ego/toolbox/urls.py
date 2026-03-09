from django.urls import path

from toolbox.views.excel_splitter import excel_splitter_preview, excel_splitter_view
from toolbox.views.feedback import feedback_view
from toolbox.views.index import index_view
from toolbox.views.removebg import removebg_view
from toolbox.views.todo import todo_view

app_name = "toolbox"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", index_view, name="index"),
    path("todo/", todo_view, name="todo"),
    path("removebg/", removebg_view, name="removebg"),
    path("excel-splitter/", excel_splitter_view, name="excel_splitter"),
    path("excel-splitter/preview/", excel_splitter_preview, name="excel_splitter_preview"),
    path("feedback/", feedback_view, name="feedback"),
]
