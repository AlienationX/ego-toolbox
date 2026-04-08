from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from toolbox.models import Todo
from toolbox.views.core.context import build_tool_context


def todo_view(request):
    if request.htmx:
        action = request.POST.get("action")

        if action == "create":
            title = request.POST.get("title")
            if title:
                todo = Todo.objects.create(title=title)
        elif action == "update":
            todo_id = request.POST.get("todo_id")
            if todo_id:
                todo = Todo.objects.get(id=todo_id)
                todo.completed = not todo.completed
                todo.save()
        elif action == "delete":
            todo_id = request.POST.get("todo_id")
            if todo_id:
                todo = Todo.objects.get(id=todo_id)
                todo.delete()

        # 重新统计数据
        todos, total_count, done_count, pending_count = _get_todo_stats()
        stats_data = {"total_count": total_count, "done_count": done_count, "pending_count": pending_count}
        stats_html = render_to_string("toolbox/partials/todo/stats.html", stats_data)
        todo_data = {"todo": todo}
        todo_html = render_to_string("toolbox/partials/todo/item.html", todo_data)

        if action == "delete":
            return HttpResponse(stats_html)  # 删除操作后只返回统计信息
        return HttpResponse(todo_html + stats_html)

    # 渲染初始页面
    todos, total_count, done_count, pending_count = _get_todo_stats()
    context = build_tool_context(
        "todo",
        todos=todos,
        total_count=total_count,
        done_count=done_count,
        pending_count=pending_count,
    )

    return render(request, "toolbox/pages/tools/productivity/todo.html", context)


def _get_todo_stats():
    todos = list(Todo.objects.order_by("-id"))
    done_count = sum(1 for todo in todos if todo.completed)
    total_count = len(todos)
    pending_count = max(total_count - done_count, 0)
    return todos, total_count, done_count, pending_count


ROUTES = [
    ("todo/", todo_view, "todo", "todo"),
]
