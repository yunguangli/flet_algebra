"""Main application class for Flet Algebra"""

import flet as ft
from coordinate_system import CoordinateSystem


class GraphingApp:
    """Main application class for the graphing application"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.coordinate_system_ref = ft.Ref[CoordinateSystem]()
        self.expr_field_ref = ft.Ref[ft.TextField]()
    
    def setup_page(self):
        """Configure page properties"""
        self.page.title = "Flet Algebra"
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.WHITE
    
    def build_ui(self):
        """Build the complete UI"""
        self.setup_page()
        
        # Create main content area
        drawer = self._create_drawer()
        appbar = self._create_top_bar()
        main_content = self._create_controls_stack()
        
        self.page.appbar = appbar
        self.page.navigation_drawer = drawer
        self.page.add(main_content)
    
    def _create_drawer(self):
        """Create navigation drawer"""
        return ft.NavigationDrawer(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=20),
                            ft.Text("Algebra Tools", weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.TextButton("Functions", on_click=lambda e: print("Functions")),
                            ft.TextButton("Equations", on_click=lambda e: print("Equations")),
                            ft.TextButton("Calculus", on_click=lambda e: print("Calculus")),
                        ],
                        tight=True,
                        spacing=0,
                    ),
                    padding=10,
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Tools", weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.TextButton("Table", on_click=lambda e: print("Table")),
                            ft.TextButton("Spreadsheet", on_click=lambda e: print("Spreadsheet")),
                        ],
                        tight=True,
                        spacing=0,
                    ),
                    padding=10,
                ),
            ]
        )
    
    def _create_top_bar(self):
        """Create top app bar"""
        def on_menu_click(e):
            self.page.navigation_drawer.open = True
            self.page.update()
        
        return ft.AppBar(
            title=ft.Text("Graphing Calculator", weight=ft.FontWeight.BOLD),
            center_title=False,
            leading=ft.IconButton(
                ft.Icons.MENU,
                on_click=on_menu_click,
            ),
            bgcolor=ft.Colors.BLUE_600,
            toolbar_height=60,
        )
    
    def _create_controls_stack(self):
        """Create the main content stack"""
        # Create coordinate system
        coord_system = CoordinateSystem(self.page)
        self.coordinate_system_ref.current = coord_system
        
        # Create expression input
        expr_field = ft.TextField(
            ref=self.expr_field_ref,
            label="f(x) = ",
            value="x**2",
            width=200,
            on_change=self._on_expr_change,
        )
        
        def on_apply_click(e):
            self._on_expr_change(None)
        
        # Create control buttons
        pan_left_btn = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self._pan_left(),
            bgcolor=ft.Colors.BLUE_400,
            mini=True,
        )
        pan_right_btn = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_FORWARD,
            on_click=lambda e: self._pan_right(),
            bgcolor=ft.Colors.BLUE_400,
            mini=True,
        )
        pan_up_btn = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_UPWARD,
            on_click=lambda e: self._pan_up(),
            bgcolor=ft.Colors.BLUE_400,
            mini=True,
        )
        pan_down_btn = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            on_click=lambda e: self._pan_down(),
            bgcolor=ft.Colors.BLUE_400,
            mini=True,
        )
        zoom_in_btn = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda e: self._zoom_in(),
            bgcolor=ft.Colors.GREEN_400,
            mini=True,
        )
        zoom_out_btn = ft.FloatingActionButton(
            icon=ft.Icons.REMOVE,
            on_click=lambda e: self._zoom_out(),
            bgcolor=ft.Colors.GREEN_400,
            mini=True,
        )
        reset_btn = ft.FloatingActionButton(
            icon=ft.Icons.REFRESH,
            on_click=lambda e: self._reset_view(),
            bgcolor=ft.Colors.ORANGE_400,
            mini=True,
        )
        
        # Create control panel
        control_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Controls", weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    expr_field,
                    ft.ElevatedButton("Apply", on_click=on_apply_click),
                    ft.Container(height=15),
                    ft.Text("Pan", weight=ft.FontWeight.W_500),
                    ft.Row(
                        controls=[pan_left_btn, pan_up_btn, pan_down_btn, pan_right_btn],
                        spacing=5,
                    ),
                    ft.Container(height=15),
                    ft.Text("Zoom", weight=ft.FontWeight.W_500),
                    ft.Row(
                        controls=[zoom_in_btn, zoom_out_btn],
                        spacing=5,
                    ),
                    ft.Container(height=15),
                    reset_btn,
                ],
                spacing=5,
            ),
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
            width=250,
        )
        
        # Create main stack
        main_stack = ft.Stack(
            expand=True,
            controls=[
                coord_system,
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                expand=True,
                                controls=[
                                    ft.Container(expand=True),
                                    control_panel,
                                    ft.Container(width=20),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                            padding=10,
                            expand=True,
                        ),
                    ],
                ),
            ],
        )
        
        return main_stack
    
    def _on_expr_change(self, e):
        """Handle expression change"""
        expr = self.expr_field_ref.current.value
        if expr:
            if self.coordinate_system_ref.current:
                self.coordinate_system_ref.current.set_expression(expr)
    
    def _pan_left(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.pan_left()
    
    def _pan_right(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.pan_right()
    
    def _pan_up(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.pan_up()
    
    def _pan_down(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.pan_down()
    
    def _zoom_in(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.zoom_in()
    
    def _zoom_out(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.zoom_out()
    
    def _reset_view(self):
        if self.coordinate_system_ref.current:
            self.coordinate_system_ref.current.reset_view()
