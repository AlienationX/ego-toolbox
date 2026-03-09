from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def feedback_image_upload_path(instance, filename):
    """反馈图片上传路径"""
    return f"feedback/{instance.id}/{filename}"


class Tool(models.Model):
    name = models.CharField(max_length=60)
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


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ("bug", _("Bug反馈")),
        ("feature", _("功能建议")),
        ("other", _("其他意见")),
    ]

    STATUS_CHOICES = [
        ("pending", _("待处理")),
        ("processing", _("处理中")),
        ("completed", _("已完成")),
    ]

    feedback_type = models.CharField(_("反馈类型"), max_length=20, choices=FEEDBACK_TYPES, default="other")
    tool_name = models.CharField(_("相关工具"), max_length=100, blank=True, default="")
    title = models.CharField(_("反馈标题"), max_length=100)
    content = models.TextField(_("详细描述"), max_length=2000)
    contact = models.CharField(_("联系方式"), max_length=200, blank=True, default="")
    image1 = models.ImageField(_("图片1"), upload_to=feedback_image_upload_path, blank=True, null=True)
    image2 = models.ImageField(_("图片2"), upload_to=feedback_image_upload_path, blank=True, null=True)
    image3 = models.ImageField(_("图片3"), upload_to=feedback_image_upload_path, blank=True, null=True)
    image4 = models.ImageField(_("图片4"), upload_to=feedback_image_upload_path, blank=True, null=True)
    image5 = models.ImageField(_("图片5"), upload_to=feedback_image_upload_path, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("IP地址"), blank=True, null=True)
    user_agent = models.CharField(_("用户代理"), max_length=500, blank=True, default="")
    status = models.CharField(_("状态"), max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(_("创建时间"), default=timezone.now)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("问题反馈")
        verbose_name_plural = _("问题反馈")
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_feedback_type_display()}] {self.title}"

    def get_images(self):
        """获取所有已上传的图片"""
        images = []
        for i in range(1, 6):
            image = getattr(self, f"image{i}")
            if image:
                images.append(image)
        return images
