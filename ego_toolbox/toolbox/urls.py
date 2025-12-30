from django.urls import path
from . import views

app_name = 'toolbox'

urlpatterns = [
    path('', views.index, name='index'),
    path('tool/<str:tool_id>/', views.tool_detail, name='tool_detail'),
]


