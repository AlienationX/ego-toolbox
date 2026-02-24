from django.db import models
from django.utils import timezone


class Tool(models.Model):
    # "id": "todo",
    # "icon": "📝",
    # "featured": True,
    # "category": "productivity",
    # "tags": [_("效率工具")],
    # "title": _("待办事项"),
    # "description": _("简单高效的待办事项管理工具，帮助你组织任务和提高效率。"),
    # "url": reverse("toolbox:todo"),

    name = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    category = models.CharField(max_length=60, default="unclassified", verbose_name="目录")
    description = models.CharField(max_length=200)
    tags = models.JSONField(verbose_name="标签")
    url = models.CharField(max_length=60, verbose_name="url地址")


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
