from django.urls import path

from toolbox.views.core.routing import discover_routes

app_name = "toolbox"

urlpatterns = [path(route["pattern"], route["view"], name=route["name"]) for route in discover_routes()]
