"""Coordinate system custom control with graph visualization"""

import flet as ft
import flet.canvas as cv
import numpy as np
from typing import List
from graph_state import GraphState, FunctionGraph


class CoordinateSystem(ft.Stack):
    """Custom composite control for the coordinate system with graph"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.expand = True
        self.state = GraphState()
        
        # Initialize controls
        self.init()
        self._is_dragging = False
    
    def init(self):
        """Initialize the coordinate system"""
        # Create canvas
        chart_canvas = cv.Canvas(
            shapes=[],
            expand=True,
        )
        
        # Store canvas reference for later updates
        self.canvas = chart_canvas
        
        # Create gesture detector for pan/zoom - wrap the canvas in it
        gesture_detector = ft.GestureDetector(
            content=chart_canvas,
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=1,
            on_pan_start=self._handle_pan_start,
            on_pan_update=self._handle_pan_update,
            on_pan_end=self._handle_pan_end,
            on_scroll=self._handle_scroll,
            expand=True,
        )
        
        # Stack contains only the gesture detector (which wraps the canvas)
        self.controls = [
            gesture_detector,
        ]
        
        # Draw initial graph after layout (defer using a timer)
        self._first_draw = True
    
    def did_mount(self):
        """Called when control is mounted to the page"""
        # Now we can safely redraw
        self.redraw()
    
    def to_screen(self, x: float, y: float) -> tuple:
        """Convert mathematical coordinates to screen coordinates"""
        canvas_width = self._page.window.width
        canvas_height = self._page.window.height
        sx = (canvas_width / 2) + self.state.offset_x + (x * self.state.scale)
        sy = (canvas_height / 2) + self.state.offset_y - (y * self.state.scale)
        return sx, sy
    
    def _handle_pan_start(self, e: ft.DragStartEvent):
        """Handle pan start - mark as dragging"""
        self._is_dragging = True
    
    def _handle_pan_update(self, e: ft.DragUpdateEvent):
        """Handle pan (drag) updates - fast update without function curve"""
        self.state.offset_x += e.local_delta.x
        self.state.offset_y += e.local_delta.y
        # During dragging, skip expensive function curve drawing for responsiveness
        self.redraw(skip_function=True)
    
    def _handle_pan_end(self, e: ft.DragEndEvent):
        """Handle pan end - do full redraw with function"""
        self._is_dragging = False
        self.redraw(skip_function=False)
    
    def _handle_scroll(self, e: ft.ScrollEvent):
        """Handle scroll for zoom"""
        zoom_factor = 1.1 if e.scroll_delta_y < 0 else 0.9
        self.state.scale *= zoom_factor
        self.redraw()
    
    def pan_up(self):
        """Pan view upward"""
        self.state.offset_y += 30
        self.redraw()
    
    def pan_down(self):
        """Pan view downward"""
        self.state.offset_y -= 30
        self.redraw()
    
    def pan_left(self):
        """Pan view left"""
        self.state.offset_x -= 30
        self.redraw()
    
    def pan_right(self):
        """Pan view right"""
        self.state.offset_x += 30
        self.redraw()
    
    def zoom_in(self):
        """Zoom in"""
        self.state.scale *= 1.2
        self.redraw()
    
    def zoom_out(self):
        """Zoom out"""
        self.state.scale *= 0.8
        self.redraw()
    
    def reset_view(self):
        """Reset view to default"""
        self.state.scale = 50.0
        self.state.offset_x = 0.0
        self.state.offset_y = 0.0
        self.redraw()
    
    def set_expression(self, expr: str):
        """Set the function expression to display"""
        self.state.expr = expr
        self.redraw()
    
    def redraw(self, skip_function: bool = False):
        """Redraw the entire canvas
        
        Args:
            skip_function: If True, skip drawing the function curve for faster updates during panning
        """
        if self.canvas:
            try:
                self.canvas.shapes = self._draw_graph(skip_function=skip_function)
                self.canvas.update()
            except Exception as e:
                # Control may not be fully added yet
                if self._first_draw:
                    self._first_draw = False
                else:
                    print(f"Redraw error: {e}")
    
    def _draw_graph(self, skip_function: bool = False) -> List:
        """Draw the complete graph with axes, grid, and function
        
        Args:
            skip_function: If True, skip drawing the function curve for faster updates
        """
        canvas_width = self._page.window.width
        canvas_height = self._page.window.height
        shapes = []
        
        # Draw grid lines
        # Set colors based on dark mode
        if self.state.dark_mode:
            grid_pen = ft.Paint(color=ft.Colors.GREY_600, stroke_width=1.5)
            minor_grid_pen = ft.Paint(color=ft.Colors.GREY_500, stroke_width=1.2)
            axis_pen_color = ft.Colors.WHITE
            tick_pen_color = ft.Colors.WHITE
            text_color = ft.Colors.WHITE
            background_color = ft.Colors.BLACK
        else:
            grid_pen = ft.Paint(color=ft.Colors.GREY_400, stroke_width=1.5)
            minor_grid_pen = ft.Paint(color=ft.Colors.GREY_300, stroke_width=1.2)
            axis_pen_color = ft.Colors.BLACK
            tick_pen_color = ft.Colors.BLACK
            text_color = ft.Colors.BLACK
            background_color = ft.Colors.WHITE
        
        # Calculate visible range in math coordinates
        # When offset_x > 0, we're panning right, so we see more negative x values
        visible_x_min = -(canvas_width / 2 + self.state.offset_x) / self.state.scale
        visible_x_max = (canvas_width / 2 - self.state.offset_x) / self.state.scale
        # When offset_y > 0, we're panning down, so we see smaller y values (more negative)
        visible_y_min = -(canvas_height / 2 - self.state.offset_y) / self.state.scale
        visible_y_max = (canvas_height / 2 + self.state.offset_y) / self.state.scale
        
        # Add padding to avoid edge artifacts
        x_min = int(np.floor(visible_x_min)) - 1
        x_max = int(np.ceil(visible_x_max)) + 1
        y_min = int(np.floor(visible_y_min)) - 1
        y_max = int(np.ceil(visible_y_max)) + 1
        
        # Major grid lines (every 2 units)
        for x in np.arange(x_min, x_max + 1, 2):
            sx, _ = self.to_screen(x, 0)
            if -10 <= sx <= canvas_width + 10:
                shapes.append(cv.Line(sx, 0, sx, canvas_height, grid_pen))
        
        for y in np.arange(y_min, y_max + 1, 2):
            _, sy = self.to_screen(0, y)
            if -10 <= sy <= canvas_height + 10:
                shapes.append(cv.Line(0, sy, canvas_width, sy, grid_pen))
        
        # Minor grid lines (every 1 unit) - only if enabled
        if self.state.show_minor_grid:
            for x in np.arange(x_min, x_max + 1, 1):
                if x % 2 != 0:  # Skip even numbers (already drawn as major grid)
                    sx, _ = self.to_screen(x, 0)
                    if -10 <= sx <= canvas_width + 10:
                        shapes.append(cv.Line(sx, 0, sx, canvas_height, minor_grid_pen))
            
            for y in np.arange(y_min, y_max + 1, 1):
                if y % 2 != 0:  # Skip even numbers (already drawn as major grid)
                    _, sy = self.to_screen(0, y)
                    if -10 <= sy <= canvas_height + 10:
                        shapes.append(cv.Line(0, sy, canvas_width, sy, minor_grid_pen))
        
        # Draw axes
        axis_pen = ft.Paint(color=axis_pen_color, stroke_width=2)
        cx, cy = self.to_screen(0, 0)
        
        # X-axis
        shapes.append(cv.Line(0, cy, canvas_width, cy, axis_pen))
        # Y-axis
        shapes.append(cv.Line(cx, 0, cx, canvas_height, axis_pen))
        
        # Draw axis arrows (at canvas edges, so they move with the axes)
        arrow_size = 10
        arrow_paint = ft.Paint(color=axis_pen_color, stroke_width=2, 
                              style=ft.PaintingStyle.FILL)
        
        # X-axis arrow (at right edge of canvas)
        x_arrow_x = canvas_width - 10
        x_arrow_y = cy
        shapes.append(cv.Path(
            [
                cv.Path.MoveTo(x_arrow_x - arrow_size, x_arrow_y - arrow_size // 2),
                cv.Path.LineTo(x_arrow_x, x_arrow_y),
                cv.Path.LineTo(x_arrow_x - arrow_size, x_arrow_y + arrow_size // 2),
            ],
            arrow_paint
        ))
        
        # Y-axis arrow (at top edge of canvas)
        y_arrow_x = cx
        y_arrow_y = 2  # Even higher, closer to the top
        shapes.append(cv.Path(
            [
                cv.Path.MoveTo(y_arrow_x - arrow_size // 2, y_arrow_y + arrow_size),
                cv.Path.LineTo(y_arrow_x, y_arrow_y),
                cv.Path.LineTo(y_arrow_x + arrow_size // 2, y_arrow_y + arrow_size),
            ],
            arrow_paint
        ))
        
        # Draw axis labels
        shapes.append(cv.Text(
            x_arrow_x - arrow_size - 15, x_arrow_y - 15, "x",
            ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=text_color)
        ))
        shapes.append(cv.Text(
            y_arrow_x + 5, y_arrow_y - 10, "y",
            ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=text_color)
        ))
        shapes.append(cv.Text(
            cx - 10, cy + 10, "0",
            ft.TextStyle(size=10, color=text_color)
        ))
        
        # Draw tick marks and labels
        tick_paint = ft.Paint(color=tick_pen_color, stroke_width=1)
        
        # Calculate dynamic label interval based on zoom level
        # At scale=50, use interval=2. At scale=5, use interval=20. Etc.
        # Label interval should be approximately 80-100 pixels apart on screen
        target_label_spacing = 80  # pixels
        label_interval = 2
        while (label_interval * self.state.scale) < target_label_spacing:
            # If labels are too close, increase interval
            if label_interval == 2:
                label_interval = 5
            elif label_interval == 5:
                label_interval = 10
            else:
                label_interval += 10
        
        # X-axis ticks and labels
        x_min = int(np.floor(visible_x_min / label_interval) * label_interval)
        x_max = int(np.ceil(visible_x_max / label_interval) * label_interval)
        
        for x in np.arange(x_min, x_max + 1, label_interval):
            if x != 0:
                sx, sy = self.to_screen(x, 0)
                if -10 <= sx <= canvas_width + 10:
                    shapes.append(cv.Line(sx, cy - 5, sx, cy + 5, tick_paint))
                    shapes.append(cv.Text(
                        sx - 5, cy + 10, str(int(x)),
                        ft.TextStyle(size=10, color=text_color)
                    ))
        
        # Y-axis ticks and labels
        y_min = int(np.floor(visible_y_min / label_interval) * label_interval)
        y_max = int(np.ceil(visible_y_max / label_interval) * label_interval)
        
        for y in np.arange(y_min, y_max + 1, label_interval):
            if y != 0:
                sx, sy = self.to_screen(0, y)
                if -10 <= sy <= canvas_height + 10:
                    shapes.append(cv.Line(cx - 5, sy, cx + 5, sy, tick_paint))
                    shapes.append(cv.Text(
                        cx - 20, sy + 5, str(int(y)),
                        ft.TextStyle(size=10, color=text_color)
                    ))
        
        # Draw the function curves (skip during fast panning for responsiveness)
        if not skip_function:
            self._draw_functions(shapes, visible_x_min, visible_x_max, 
                                canvas_width, canvas_height)
        
        return shapes
    
    def _draw_functions(self, shapes: List, x_min: float, x_max: float, 
                       canvas_width: float, canvas_height: float):
        """Draw all function curves"""
        # Color palette for multiple functions
        # Use brighter colors in dark mode
        if self.state.dark_mode:
            colors = [
                ft.Colors.RED_400,
                ft.Colors.BLUE_400,
                ft.Colors.GREEN_400,
                ft.Colors.ORANGE_400,
                ft.Colors.PURPLE_400,
            ]
        else:
            colors = [
                ft.Colors.RED,
                ft.Colors.BLUE,
                ft.Colors.GREEN,
                ft.Colors.ORANGE,
                ft.Colors.PURPLE,
            ]
        
        # Draw each expression
        for i, expr in enumerate(self.state.expressions):
            color = colors[i % len(colors)]
            self._draw_function(shapes, expr, x_min, x_max, 
                              canvas_width, canvas_height, color)
    
    def _draw_function(self, shapes: List, expr: str, x_min: float, x_max: float, 
                      canvas_width: float, canvas_height: float, 
                      color: str = ft.Colors.RED):
        """Draw a single function curve"""
        try:
            curve_paint = ft.Paint(
                color=color,
                stroke_width=3,
                style=ft.PaintingStyle.STROKE
            )
            
            # Sample points
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = FunctionGraph.evaluate(expr, x_vals)
            
            # Create and add path
            path_elements = FunctionGraph.create_path(
                x_vals, y_vals, self.to_screen
            )
            
            if path_elements:
                shapes.append(cv.Path(path_elements, curve_paint))
        except Exception as e:
            print(f"Graph drawing error: {e}")
