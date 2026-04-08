from functools import lru_cache
from importlib import import_module
from pkgutil import walk_packages

import toolbox.views


def _normalize_route(route):
    if isinstance(route, dict):
        return route

    if len(route) == 3:
        pattern, view, name = route
        return {"pattern": pattern, "view": view, "name": name}

    if len(route) == 4:
        pattern, view, name, tool_id = route
        return {"pattern": pattern, "view": view, "name": name, "tool_id": tool_id}

    raise ValueError(f"Unsupported route metadata: {route!r}")


@lru_cache(maxsize=1)
def discover_routes():
    routes = []
    modules = sorted(walk_packages(toolbox.views.__path__, toolbox.views.__name__ + "."), key=lambda item: item.name)
    for module_info in modules:
        if module_info.ispkg:
            continue
        module = import_module(module_info.name)
        routes.extend(_normalize_route(route) for route in getattr(module, "ROUTES", []))
    return routes


@lru_cache(maxsize=1)
def get_tool_route_name_map():
    return {route["tool_id"]: route["name"] for route in discover_routes() if route.get("tool_id")}
