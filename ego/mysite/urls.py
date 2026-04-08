"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .error_views import bad_request, not_found, server_error
from .views import login_view, logout_view, register_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("login/", login_view, name="my_login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    # 单应用配置，将 toolbox 应用路由到 / url下
    path("", include("toolbox.urls", namespace="toolbox")),
    # 多应用配置，将 toolbox 应用路由到 /toolbox/ url下
    # path("toolbox/", include("toolbox.urls", namespace="toolbox")),
]

# 自定义错误页面
handler400 = bad_request
handler404 = not_found
handler500 = server_error

# 在开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
