from django.urls import path
from . import views

app_name = 'toolbox'

urlpatterns = [
    path('', views.index, name='index'),
    path('tool/<str:tool_id>/', views.tool_detail, name='tool_detail'),
    # 语言切换路由
    path('custom_set_language/', views.custom_set_language, name='custom_set_language'),
    # 待办事项相关路由
    path('todo/add/', views.todo_add, name='todo_add'),
    path('todo/<int:todo_id>/toggle/', views.todo_toggle, name='todo_toggle'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
    path('todo/', views.todo_detail, name='todo_detail'),
]


