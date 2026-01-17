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
        self.bottom_appbar_ref = ft.Ref[ft.BottomAppBar]()
        self.functions_list_ref = ft.Ref[ft.ListView]()
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
        
        # Then create appbar and bottomappbar
        appbar = self._create_top_bar()
        main_content = self._create_controls_stack()
        bottom_appbar = self._create_bottom_appbar()
        
        self.page.appbar = appbar
        self.page.bottom_appbar = bottom_appbar
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
        """Create top app bar with popup menu for grid and reset"""
        async def on_menu_click(e):
            await self.page.show_drawer()
        
        def on_reset_click(e):
            """Reset view from menu"""
            self._reset_view()
        
        # Create grid toggle menu item with indicator
        # Store the checkmark icon reference so we can update its visibility
        checkmark_icon = ft.Icon(
            ft.Icons.CHECK,
            size=20,
            color=ft.Colors.GREEN,
            visible=True,  # Initially visible since show_minor_grid starts as True
        )
        
        def on_grid_toggle_click(e):
            """Toggle minor grid from menu"""
            if self.coordinate_system_ref.current:
                current_state = self.coordinate_system_ref.current.state.show_minor_grid
                self.coordinate_system_ref.current.state.show_minor_grid = not current_state
                checkmark_icon.visible = not current_state  # Update checkmark visibility
                self.coordinate_system_ref.current.redraw()
                self.page.update()
        
        grid_menu_item = ft.PopupMenuItem(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.GRID_ON, size=20),
                    ft.Text("Toggle Grid", expand=True),
                    checkmark_icon,
                ],
                spacing=10,
            ),
            on_click=on_grid_toggle_click,
        )
        
        return ft.AppBar(
            title=ft.Text("Graphing Calculator", weight=ft.FontWeight.BOLD),
            center_title=False,
            leading=ft.IconButton(
                ft.Icons.MENU,
                on_click=on_menu_click,
            ),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        grid_menu_item,
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            content="Reset View",
                            icon=ft.Icons.REFRESH,
                            on_click=on_reset_click,
                        ),
                    ]
                ),
            ],
            bgcolor=ft.Colors.BLUE_600,
            toolbar_height=60,
        )
    
    def _create_bottom_appbar(self):
        """Create bottom app bar with pan and zoom buttons (initially invisible)"""
        def on_close_bottom_appbar(e):
            if self.bottom_appbar_ref.current:
                self.bottom_appbar_ref.current.visible = False
                self.page.update()
        
        return ft.BottomAppBar(
            ref=self.bottom_appbar_ref,
            bgcolor=ft.Colors.BLUE_600,
            visible=False,  # Initially invisible
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._pan_left(),
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_UPWARD,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._pan_up(),
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_DOWNWARD,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._pan_down(),
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_FORWARD,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._pan_right(),
                    ),
                    ft.IconButton(
                        ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._zoom_in(),
                    ),
                    ft.IconButton(
                        ft.Icons.REMOVE,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self._zoom_out(),
                    ),
                    ft.IconButton(
                        ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        on_click=on_close_bottom_appbar,
                    ),
                ],
            ),
        )
    
    def _create_controls_stack(self):
        """Create the main content stack"""
        # Create coordinate system
        coord_system = CoordinateSystem(self.page)
        self.coordinate_system_ref.current = coord_system
        
        # Initialize with the default expression
        coord_system.state.expressions = ["x**2"]
        
        # Create expression input with ListView for multiple functions
        expr_field = ft.TextField(
            ref=self.expr_field_ref,
            label="f(x) = ",
            value="x**2",
            width=200,
            on_change=self._on_expr_change,
        )
        
        def create_function_item(expr_text: str = ""):
            """Create a function input row with remove (-) and submit (+) buttons"""
            text_field = ft.TextField(
                label="f(x) = ",
                value=expr_text,
                width=180,
            )
            
            # Create the row first so we can reference it in the remove function
            item_row = None
            submit_button = None
            
            def on_apply_function(e):
                expr = text_field.value
                if expr and self.coordinate_system_ref.current:
                    # Add to expressions list
                    if expr not in self.coordinate_system_ref.current.state.expressions:
                        self.coordinate_system_ref.current.state.expressions.append(expr)
                    self.coordinate_system_ref.current.redraw()
            
            def on_remove_function(e):
                expr = text_field.value
                # Remove from expressions list
                if expr and self.coordinate_system_ref.current:
                    if expr in self.coordinate_system_ref.current.state.expressions:
                        self.coordinate_system_ref.current.state.expressions.remove(expr)
                    self.coordinate_system_ref.current.redraw()
                
                # Remove from ListView
                if item_row and self.functions_list_ref.current:
                    if item_row in self.functions_list_ref.current.controls:
                        self.functions_list_ref.current.controls.remove(item_row)
                        self.page.update()
            
            def on_text_change(e):
                """Enable/disable submit button based on text input"""
                if submit_button:
                    submit_button.disabled = not text_field.value
                    self.page.update()
            
            # Set on_submit to call same function as the button
            text_field.on_submit = on_apply_function
            text_field.on_change = on_text_change
            
            submit_button = ft.IconButton(
                ft.Icons.ADD,
                icon_color=ft.Colors.GREEN,
                on_click=on_apply_function,
                disabled=not expr_text,  # Disable if no initial text
            )
            
            item_row = ft.Row(
                controls=[
                    ft.IconButton(
                        ft.Icons.REMOVE,
                        icon_color=ft.Colors.RED,
                        on_click=on_remove_function,
                    ),
                    text_field,
                    submit_button,
                ],
                spacing=5,
            )
            
            return item_row
        
        def on_add_function(e):
            """Add a new function input field"""
            if self.functions_list_ref.current:
                self.functions_list_ref.current.controls.append(create_function_item())
                self.page.update()
        
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
        
        # Create ListView for multiple functions
        functions_list = ft.ListView(
            ref=self.functions_list_ref,
            controls=[],
            spacing=10,
            padding=10,
            height=self.page.height,
        )
        
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
        
        # Create control panel (initially invisible) with ListView for functions
        control_panel = ft.Container(
            ref=self.control_panel_ref,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Functions", weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ft.Icons.CLOSE,
                                on_click=on_close_click,
                                icon_size=20,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=5),

                    ft.Button(
                        "Add Function",
                        icon=ft.Icons.ADD,
                        on_click=on_add_function,
                        width=230,
                    ),
                    ft.Container(height=10),
                    functions_list,
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
        def on_coordinate_long_press(e):
            """Show bottom app bar on long press"""
            if self.bottom_appbar_ref.current:
                self.bottom_appbar_ref.current.visible = True
                self.page.update()
        
        # Wrap coordinate system with gesture detector for long-press only
        # The coordinate system itself handles pan/zoom events
        coord_system_wrapper = ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    content=coord_system,
                    expand=True,
                    padding=10,
                ),
                ft.GestureDetector(
                    on_long_press=on_coordinate_long_press,
                    expand=True,
                ),
            ],
        )
        
        main_content = ft.Row(
            expand=True,
            controls=[
                # Left side: Control panel
                control_panel,
                ft.Container(width=10),  # Spacer
                # Right side: Coordinate system
                coord_system_wrapper,
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
