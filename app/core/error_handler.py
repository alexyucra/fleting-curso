
import flet as ft
from core.logger import get_logger

logger = get_logger("ErrorHandler")

class GlobalErrorHandler:
    @staticmethod
    def handle(page: ft.Page, error: Exception):
        logger.exception("Global error caught")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("⚠️ An error occurred.", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Something went wrong. Please try again."),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        )
        page.update()
