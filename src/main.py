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
    
    # Create coordinate system using Matplotlib for better visualization
    import matplotlib.pyplot as plt
    import numpy as np
    import flet_charts as fch
    
    # Store axis limits for dynamic updating
    xlim_min = -10
    xlim_max = 10
    ylim_min = -10
    ylim_max = 10
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Move the bottom and left spines to the origin (data coordinate 0,0)
    # 'zero' means position at data coordinate 0, not at the center
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    
    # Hide the top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Set axis limits
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylim(ylim_min, ylim_max)
    
    # Add arrows to the end of the axes using patches for better control
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.transforms import blended_transform_factory
    
    # Store references for updating in a mutable container
    arrows = {}
    
    # X-arrow: points to the right edge (xlim_max) at y=0
    x_arrow_patch = FancyArrowPatch((xlim_max - 0.5, 0), (xlim_max, 0),
                                   arrowstyle='->', mutation_scale=20, color='black', lw=1.5, clip_on=False)
    # Y-arrow: points to the top edge (ylim_max) at x=0
    y_arrow_patch = FancyArrowPatch((0, ylim_max - 0.5), (0, ylim_max),
                                   arrowstyle='->', mutation_scale=20, color='black', lw=1.5, clip_on=False)
    arrows['x'] = x_arrow_patch
    arrows['y'] = y_arrow_patch
    ax.add_patch(x_arrow_patch)
    ax.add_patch(y_arrow_patch)
    
    # Set axis labels at the tips
    # X-axis label at the rightmost tip (xlim_max) slightly below
    x_label = ax.text(xlim_max, -0.8, 'x', fontsize=12, ha='center', va='top', fontweight='bold')
    # Y-axis label at the topmost tip (ylim_max) slightly to the right
    y_label = ax.text(0.8, ylim_max, 'y', fontsize=12, ha='left', va='center', fontweight='bold')
    
    # Set tick labels
    ax.set_xticks(np.arange(-10, 11, 2))
    ax.set_yticks(np.arange(-10, 11, 2))
    
    # Customize tick labels to show only one '0' at the origin
    # Set tick positions to be on the left and bottom axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Create new labels list for the x-axis, replacing the '0' with an empty string
    new_xticks_labels = [label.get_text().replace('−', '-') if label.get_text().replace('−', '-') != '0' else ''
                          for label in ax.get_xticklabels()]
    ax.set_xticklabels(new_xticks_labels)
    
    # Create new labels list for the y-axis, replacing the '0' with an empty string
    new_yticks_labels = [label.get_text().replace('−', '-') if label.get_text().replace('−', '-') != '0' else ''
                          for label in ax.get_yticklabels()]
    ax.set_yticklabels(new_yticks_labels)
    
    # Manually add a single '0' annotation at the origin (0,0) position
    # The (0,0) in `xy` is the data coordinate, and `xytext` is an offset for positioning
    zero_annotation = ax.annotate('0', xy=(0, 0), xytext=(-5, -10), textcoords='offset points', ha='right', va='top')
    
    # Add grid lines (optional, for graph paper look)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    
    # Create coordinate chart using Matplotlib
    coordinate_chart = fch.MatplotlibChart(
        figure=fig,
        expand=True,
    )
    
    coordinate_container = ft.Container(
        content=coordinate_chart,
        width=800,
        height=600,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.GREY_300),
    )
    
    # Event handlers for GestureDetector
    def handle_pan_update(e: ft.DragUpdateEvent[ft.GestureDetector]):
        """Handle pan (drag) updates on the coordinate system.
        
        When user drags the mouse:
        - Dragging right moves the view right (coordinates move left)
        - Dragging left moves the view left (coordinates move right)
        - Dragging down moves the view down (coordinates move up)
        - Dragging up moves the view up (coordinates move down)
        """
        nonlocal xlim_min, xlim_max, ylim_min, ylim_max
        
        # Get drag deltas
        dx = e.local_delta.x
        dy = e.local_delta.y
        
        # Calculate data coordinate shifts based on canvas size and current range
        data_range_x = xlim_max - xlim_min
        data_range_y = ylim_max - ylim_min
        
        # Convert pixel movement to data coordinates
        # Canvas is 800x600. Positive dx right means move the view right (shift limits left)
        shift_x = -(dx / 800) * data_range_x
        shift_y = (dy / 600) * data_range_y  # Y is inverted
        
        # Update limits
        xlim_min += shift_x
        xlim_max += shift_x
        ylim_min += shift_y
        ylim_max += shift_y
        
        # Set new axis limits
        ax.set_xlim(xlim_min, xlim_max)
        ax.set_ylim(ylim_min, ylim_max)
        
        # Remove old arrows and create new ones at updated positions
        arrows['x'].remove()
        arrows['y'].remove()
        
        from matplotlib.patches import FancyArrowPatch
        # X-arrow always ends at xlim_max (right edge) at y=0
        x_arrow_patch_new = FancyArrowPatch((xlim_max - 0.5, 0), (xlim_max, 0),
                                           arrowstyle='->', mutation_scale=20, color='black', lw=1.5, clip_on=False)
        # Y-arrow always ends at ylim_max (top edge) at x=0
        y_arrow_patch_new = FancyArrowPatch((0, ylim_max - 0.5), (0, ylim_max),
                                           arrowstyle='->', mutation_scale=20, color='black', lw=1.5, clip_on=False)
        ax.add_patch(x_arrow_patch_new)
        ax.add_patch(y_arrow_patch_new)
        
        # Update the dictionary references
        arrows['x'] = x_arrow_patch_new
        arrows['y'] = y_arrow_patch_new
        
        # Update axis labels to stay at the arrow tips
        # X-label stays near the tip of x-arrow (at xlim_max, offset below the axis)
        x_label.set_position((xlim_max, -0.8))
        # Y-label stays near the tip of y-arrow (offset right from y-axis, at ylim_max)
        y_label.set_position((0.8, ylim_max))
        
        # Update tick positions and labels
        tick_step = 2
        
        # Calculate new tick positions
        x_tick_min = np.floor(xlim_min / tick_step) * tick_step
        x_tick_max = np.ceil(xlim_max / tick_step) * tick_step
        new_xticks = np.arange(x_tick_min, x_tick_max + tick_step, tick_step)
        
        y_tick_min = np.floor(ylim_min / tick_step) * tick_step
        y_tick_max = np.ceil(ylim_max / tick_step) * tick_step
        new_yticks = np.arange(y_tick_min, y_tick_max + tick_step, tick_step)
        
        ax.set_xticks(new_xticks)
        ax.set_yticks(new_yticks)
        
        # Format tick labels - hide 0 from ticks, we'll add it separately
        x_labels = [f'{int(x)}' if x != 0 else '' for x in new_xticks]
        y_labels = [f'{int(y)}' if y != 0 else '' for y in new_yticks]
        
        ax.set_xticklabels(x_labels)
        ax.set_yticklabels(y_labels)
        
        # Update '0' annotation at origin
        zero_annotation.set_position((0, 0))
        
        # Force complete redraw
        fig.canvas.draw_idle()
        coordinate_chart.update()
    
    # Create transparent container for gesture detection
    transparent_container = ft.Container(
        width=800,
        height=600,
        bgcolor=ft.Colors.TRANSPARENT,
    )
    
    # Wrap transparent container in GestureDetector for dragging
    gesture_detector = ft.GestureDetector(
        content=transparent_container,
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=handle_pan_update,
    )
    
    # Stack coordinate chart and transparent gesture detector
    stack = ft.Stack(
        width=800,
        height=600,
        controls=[
            coordinate_container,
            gesture_detector,
        ],
    )
    
    # Wrap in InteractiveViewer for zoom and pan
    coordinate_system = ft.InteractiveViewer(
        content=stack,
        min_scale=0.5,
        max_scale=5.0,
        boundary_margin=ft.Margin.all(100),
    )
    
    # Create top bar
    async def handle_menu_click(e):
        await page.show_drawer()
    
    top_bar = ft.AppBar(
        title=ft.Text("Algebra Visualization", color=ft.Colors.WHITE),
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