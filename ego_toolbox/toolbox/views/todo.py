from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from ..models import Todo
from .catalog import get_nav_categories, get_tool_catalog


def todo_view(request):
    if request.htmx:
        action = request.POST.get("action")

        if action == "create":
            title = request.POST.get("title")
            if title:
                todo = Todo.objects.create(title=title)
                html = render_to_string("toolbox/todo_item.html", {"todo": todo})
                return HttpResponse(html)
        elif action == "update":
            todo_id = request.POST.get("todo_id")
            if todo_id:
                todo = Todo.objects.get(id=todo_id)
                todo.completed = not todo.completed
                todo.save()
                html = render_to_string("toolbox/todo_item.html", {"todo": todo})
                return HttpResponse(html)
        elif action == "delete":
            todo_id = request.POST.get("todo_id")
            if todo_id:
                todo = Todo.objects.get(id=todo_id)
                todo.delete()
                return HttpResponse("")

    todos = list(Todo.objects.order_by("-id"))
    done_count = sum(1 for todo in todos if todo.completed)
    total_count = len(todos)
    all_tools = get_tool_catalog()

    todo_info = {
        "id": "todo",
        "title": _("待办事项"),
        "description": _("简单高效的任务管理，帮助你掌控每天节奏。"),
        "icon": "📝",
    }

    context = {
        "tool": todo_info,
        "todos": todos,
        "done_count": done_count,
        "total_count": total_count,
        "pending_count": max(total_count - done_count, 0),
        "nav_categories": get_nav_categories(all_tools),
    }
    return render(request, "toolbox/todo.html", context)
