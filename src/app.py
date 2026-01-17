"""Main application class for Flet Algebra"""

import flet as ft
from coordinate_system import CoordinateSystem


class GraphingApp:
    """Main application class for the graphing application"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.coordinate_system_ref = ft.Ref[CoordinateSystem]()
        self.expr_field_ref = ft.Ref[ft.TextField]()
        self.control_panel_ref = ft.Ref[ft.Container]()
        self.drawer = None  # Store drawer reference
    
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
        
        # Create drawer first and set it on page BEFORE creating appbar
        self.drawer = self._create_drawer()
        self.page.drawer = self.drawer  # Use page.drawer, not navigation_drawer
        
        # Then create appbar
        appbar = self._create_top_bar()
        main_content = self._create_controls_stack()
        
        self.page.appbar = appbar
        self.page.add(main_content)
    
    def _create_drawer(self):
        """Create navigation drawer"""
        async def handle_drawer_change(e: ft.NavigationDrawer):
            """Handle drawer item selection"""
            selected = e.control.selected_index
            # Show controls panel when Functions (index 0) is selected
            if selected == 0 and self.control_panel_ref.current:
                self.control_panel_ref.current.visible = True
                self.page.update()
            await self.page.close_drawer()
        
        async def handle_drawer_dismiss(e):
            """Handle drawer dismissal"""
            print("Drawer dismissed!")
        
        return ft.NavigationDrawer(
            on_change=handle_drawer_change,
            on_dismiss=handle_drawer_dismiss,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Functions",
                    icon=ft.Icons.FUNCTIONS_OUTLINED,
                    selected_icon=ft.Icons.FUNCTIONS,
                ),
                ft.NavigationDrawerDestination(
                    label="Equations",
                    icon=ft.Icons.EQUALIZER_OUTLINED,
                    selected_icon=ft.Icons.EQUALIZER,
                ),
                ft.NavigationDrawerDestination(
                    label="Calculus",
                    icon=ft.Icons.AUTO_GRAPH_OUTLINED,
                    selected_icon=ft.Icons.AUTO_GRAPH,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Table",
                    icon=ft.Icons.TABLE_CHART_OUTLINED,
                    selected_icon=ft.Icons.TABLE_CHART,
                ),
                ft.NavigationDrawerDestination(
                    label="Spreadsheet",
                    icon=ft.Icons.GRID_ON_OUTLINED,
                    selected_icon=ft.Icons.GRID_ON,
                ),
            ]
        )
    
    def _create_top_bar(self):
        """Create top app bar"""
        async def on_menu_click(e):
            await self.page.show_drawer()
        
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
        
        def on_close_click(e):
            if self.control_panel_ref.current:
                self.control_panel_ref.current.visible = False
                self.page.update()
        
        def on_grid_toggle(e):
            if self.coordinate_system_ref.current:
                new_value = e.control.value
                self.coordinate_system_ref.current.state.show_minor_grid = new_value
                self.coordinate_system_ref.current.redraw()
                self.page.update()
        
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
        
        # Create control panel (initially invisible)
        control_panel = ft.Container(
            ref=self.control_panel_ref,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Controls", weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ft.Icons.CLOSE,
                                on_click=on_close_click,
                                icon_size=20,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    expr_field,
                    ft.Button("Apply", on_click=on_apply_click),
                    ft.Container(height=15),
                    ft.Text("Grid", weight=ft.FontWeight.W_500),
                    ft.Row(
                        controls=[
                            ft.Text("Minor Grid:", size=11),
                            ft.Switch(value=True, on_change=on_grid_toggle),
                        ],
                        spacing=10,
                    ),
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
            visible=False,  # Initially invisible
        )
        
        # Create main stack with left control panel and right coordinate system
        main_content = ft.Row(
            expand=True,
            controls=[
                # Left side: Control panel
                control_panel,
                ft.Container(width=10),  # Spacer
                # Right side: Coordinate system
                ft.Container(
                    content=coord_system,
                    expand=True,
                    padding=10,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        return main_content
    
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
