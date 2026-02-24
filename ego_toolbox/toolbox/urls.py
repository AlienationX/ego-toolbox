from django.urls import path
from toolbox.views.index import index_view
from toolbox.views.todo import todo_view

app_name = "toolbox"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", index_view, name="index"),
    # path("tool/<str:tool_id>/", views.tool_detail, name="tool_detail"),
    path("todo/", todo_view, name="todo"),
]
