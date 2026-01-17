"""Temporary script to create main.py"""

content = '''"""Entry point for Flet Algebra application"""

import flet as ft
from app import GraphingApp


def main(page: ft.Page):
    """Main entry point"""
    app = GraphingApp(page)
    app.build_ui()


if __name__ == "__main__":
    ft.app(target=main)
'''

with open('main.py', 'w') as f:
    f.write(content)

print("main.py created successfully")
