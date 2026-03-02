from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tool(models.Model):
    # "id": "todo",
    # "icon": "📝",
    # "featured": True,
    # "category": "productivity",
    # "tags": [_("效率工具")],
    # "title": _("待办事项"),
    # "description": _("简单高效的待办事项管理工具，帮助你组织任务和提高效率。"),
    # "url": reverse("toolbox:todo"),

    name = models.CharField(max_length=60)  # 英文名称，唯一标识
    title = models.CharField(_("标题"), max_length=60)
    category = models.CharField(_("分类"), max_length=60, default="unclassified")
    description = models.CharField(_("描述"), max_length=200)
    tags = models.JSONField(_("标签"))
    url = models.CharField(_("url地址"), max_length=60)
    status = models.BooleanField(_("状态"), default=False)

    def __str__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
