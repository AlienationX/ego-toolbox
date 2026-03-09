from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "feedback_type", "title", "tool_name", "status", "created_at", "ip_address"]
    list_filter = ["feedback_type", "status", "created_at"]
    search_fields = ["title", "content", "contact", "ip_address"]
    readonly_fields = ["created_at", "updated_at", "ip_address", "user_agent"]
    ordering = ["-created_at"]
    
    fieldsets = (
        (_("基本信息"), {
            "fields": ("feedback_type", "tool_name", "title", "content", "contact")
        }),
        (_("图片附件"), {
            "fields": ("image1", "image2", "image3", "image4", "image5")
        }),
        (_("状态信息"), {
            "fields": ("status",)
        }),
        (_("系统信息"), {
            "fields": ("ip_address", "user_agent", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_images(self, obj):
        """获取所有图片"""
        images = obj.get_images()
        if not images:
            return "-"
        return ", ".join([str(img) for img in images])
    get_images.short_description = _("图片")
