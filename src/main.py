"""Entry point for Flet Algebra application"""

import flet as ft
from app import GraphingApp


def main(page: ft.Page):
    """Main entry point"""
    app = GraphingApp(page)
    app.build_ui()


if __name__ == "__main__":
    ft.run(main)
