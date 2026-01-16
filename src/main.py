import flet as ft

def main(page: ft.Page):
    # Set page properties
    page.title = "GeoGebra Calculator Suite"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    page.bgcolor = ft.Colors.WHITE
    
    # Create navigation drawer items
    drawer_items = [
        ft.Container(height=12),
        ft.NavigationDrawerDestination(
            label="Algebra",
            icon=ft.Icons.ADD_OUTLINED,
            selected_icon=ft.Icons.ADD,
        ),
        ft.NavigationDrawerDestination(
            label="Tools",
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icons.SETTINGS,
        ),
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
    
    # Create navigation drawer
    def handle_drawer_dismiss(e: ft.Event[ft.NavigationDrawer]):
        print("Drawer dismissed!")
    
    async def handle_drawer_change(e: ft.Event[ft.NavigationDrawer]):
        print(f"Selected Index changed: {e.control.selected_index}")
        await page.close_drawer()
    
    navigation_drawer = ft.NavigationDrawer(
        controls=drawer_items,
        on_dismiss=handle_drawer_dismiss,
        on_change=handle_drawer_change,
    )
    
    # Create coordinate system using LineChart for zoom/pan
    import flet_charts as fch
    
    # Create grid lines data series
    grid_lines = []
    
    # Vertical grid lines
    for i in range(-10, 11):
        grid_lines.append(
            fch.LineChartData(
                stroke_width=1,
                color=ft.Colors.GREY_300,
                curved=False,
                points=[
                    fch.LineChartDataPoint(i, -10),
                    fch.LineChartDataPoint(i, 10),
                ],
            )
        )
    
    # Horizontal grid lines
    for i in range(-10, 11):
        grid_lines.append(
            fch.LineChartData(
                stroke_width=1,
                color=ft.Colors.GREY_300,
                curved=False,
                points=[
                    fch.LineChartDataPoint(-10, i),
                    fch.LineChartDataPoint(10, i),
                ],
            )
        )
    
    # Create coordinate chart
    coordinate_chart = fch.LineChart(
        expand=True,
        data_series=grid_lines,
        min_x=-10,
        max_x=10,
        min_y=-10,
        max_y=10,
        border=ft.Border.all(2, ft.Colors.BLACK),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=1, color=ft.Colors.GREY_300, width=1
        ),
        vertical_grid_lines=fch.ChartGridLines(
            interval=1, color=ft.Colors.GREY_300, width=1
        ),
        interactive=True,
    )
    
    coordinate_container = ft.Container(
        content=coordinate_chart,
        width=800,
        height=600,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.GREY_300),
    )
    
    # Wrap in InteractiveViewer for zoom and pan
    coordinate_system = ft.InteractiveViewer(
        content=coordinate_container,
        min_scale=0.5,
        max_scale=5.0,
        boundary_margin=ft.Margin.all(100),
    )
    
    # Create top bar
    async def handle_menu_click(e):
        await page.show_drawer()
    
    top_bar = ft.AppBar(
        title=ft.Text("GeoGebra Calculator Suite", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE,
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=handle_menu_click),
        actions=[
            ft.IconButton(icon=ft.Icons.GRAPHIC_EQ),
            ft.Dropdown(
                width=150,
                options=[
                    ft.dropdown.Option("Graphing"),
                    ft.dropdown.Option("Algebra"),
                    ft.dropdown.Option("Geometry"),
                ],
            ),
            ft.IconButton(icon=ft.Icons.SHARE),
            ft.TextButton(content=ft.Text("ASSIGN", color=ft.Colors.WHITE)),
            ft.TextButton(content=ft.Text("SIGN IN", color=ft.Colors.WHITE)),
        ],
    )
    
    # Create input field
    input_field = ft.TextField(
        hint_text="Input...",
        width=300,
        border=ft.InputBorder.NONE,
    )
    
    # Main content
    main_content = ft.Column(
        controls=[
            top_bar,
            ft.Container(
                expand=True,
                content=coordinate_system,
                padding=20,
            ),
        ],
        expand=True,
    )
    
    # Set the drawer on the page
    page.drawer = navigation_drawer
    
    # Add the main content to the page
    page.add(main_content)

if __name__ == "__main__":
    ft.run(main)