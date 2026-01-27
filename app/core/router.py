
import flet as ft
from core.logger import get_logger

logger = get_logger("Router")
class Router:
    def __init__(self, page):
        self.page = page
        self.current_route = "/"
        self.routes = self._load_routes()

    def _load_routes(self):
        from configs.routes import routes
        return routes

    def navigate(self, route):
        routes = self.routes

        if route not in routes:
            logger.warning(f"Route not found: {route}")
            route = "/"

        logger.info(f"Navigating to: {route}")
        self.current_route = route
        self.page.controls.clear()

        try:
            view = routes[route](self.page, self)
            self.page.add(view)
        except Exception as e:
            logger.exception("Error rendering view")
            self.page.add(ft.Text("Internal application error"))

        self.page.update()
