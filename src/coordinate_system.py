"""Coordinate system custom control with graph visualization"""

import flet as ft
import flet.canvas as cv
import numpy as np
from typing import List
from models import GraphState, FunctionGraph


class CoordinateSystem(ft.Stack):
    """Custom composite control for the coordinate system with graph"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.expand = True
        self.state = GraphState()
        
        # Initialize controls
        self.init()
    
    def init(self):
        """Initialize the coordinate system"""
        # Create canvas
        chart_canvas = cv.Canvas(
            shapes=[],
            expand=True,
        )
        
        # Store canvas reference for later updates
        self.canvas = chart_canvas
        
        # Create gesture detector for pan/zoom
        gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=10,
            on_pan_update=self._handle_pan_update,
            on_scroll=self._handle_scroll,
            expand=True,
        )
        
        # Stack canvas and gesture detector
        self.controls = [
            chart_canvas,
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
    
    def _handle_pan_update(self, e: ft.DragUpdateEvent):
        """Handle pan (drag) updates"""
        self.state.offset_x += e.local_delta.x
        self.state.offset_y += e.local_delta.y
        self.redraw()
    
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
    
    def redraw(self):
        """Redraw the entire canvas"""
        if self.canvas:
            try:
                self.canvas.shapes = self._draw_graph()
                self.canvas.update()
            except Exception as e:
                # Control may not be fully added yet
                if self._first_draw:
                    self._first_draw = False
                else:
                    print(f"Redraw error: {e}")
    
    def _draw_graph(self) -> List:
        """Draw the complete graph with axes, grid, and function"""
        canvas_width = self._page.window.width
        canvas_height = self._page.window.height
        shapes = []
        
        # Draw grid lines
        grid_pen = ft.Paint(color=ft.Colors.GREY_300, stroke_width=1)
        minor_grid_pen = ft.Paint(color=ft.Colors.GREY_100, stroke_width=0.5)
        
        # Calculate visible range
        visible_x_min = -(canvas_width / 2 - self.state.offset_x) / self.state.scale
        visible_x_max = (canvas_width / 2 + self.state.offset_x) / self.state.scale
        visible_y_min = -(canvas_height / 2 + self.state.offset_y) / self.state.scale
        visible_y_max = (canvas_height / 2 - self.state.offset_y) / self.state.scale
        
        # Major grid lines (every 2 units)
        for x in np.arange(-20, 21, 2):
            sx, _ = self.to_screen(x, 0)
            if 0 <= sx <= canvas_width:
                shapes.append(cv.Line(sx, 0, sx, canvas_height, grid_pen))
        
        for y in np.arange(-20, 21, 2):
            _, sy = self.to_screen(0, y)
            if 0 <= sy <= canvas_height:
                shapes.append(cv.Line(0, sy, canvas_width, sy, grid_pen))
        
        # Minor grid lines (every 1 unit)
        for x in np.arange(-20, 21, 1):
            sx, _ = self.to_screen(x, 0)
            if 0 <= sx <= canvas_width and x % 2 != 0:
                shapes.append(cv.Line(sx, 0, sx, canvas_height, minor_grid_pen))
        
        for y in np.arange(-20, 21, 1):
            _, sy = self.to_screen(0, y)
            if 0 <= sy <= canvas_height and y % 2 != 0:
                shapes.append(cv.Line(0, sy, canvas_width, sy, minor_grid_pen))
        
        # Draw axes
        axis_pen = ft.Paint(color=ft.Colors.BLACK, stroke_width=2)
        cx, cy = self.to_screen(0, 0)
        
        # X-axis
        shapes.append(cv.Line(0, cy, canvas_width, cy, axis_pen))
        # Y-axis
        shapes.append(cv.Line(cx, 0, cx, canvas_height, axis_pen))
        
        # Draw axis arrows
        arrow_size = 10
        arrow_paint = ft.Paint(color=ft.Colors.BLACK, stroke_width=2, 
                              style=ft.PaintingStyle.FILL)
        
        # X-axis arrow (right)
        x_arrow_x, x_arrow_y = self.to_screen(visible_x_max, 0)
        shapes.append(cv.Path(
            [
                cv.Path.MoveTo(x_arrow_x - arrow_size, x_arrow_y - arrow_size // 2),
                cv.Path.LineTo(x_arrow_x, x_arrow_y),
                cv.Path.LineTo(x_arrow_x - arrow_size, x_arrow_y + arrow_size // 2),
            ],
            arrow_paint
        ))
        
        # Y-axis arrow (top)
        y_arrow_x, y_arrow_y = self.to_screen(0, visible_y_max)
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
            x_arrow_x - arrow_size, x_arrow_y - 15, "x",
            ft.TextStyle(size=12, weight=ft.FontWeight.BOLD)
        ))
        shapes.append(cv.Text(
            y_arrow_x + 5, y_arrow_y + arrow_size, "y",
            ft.TextStyle(size=12, weight=ft.FontWeight.BOLD)
        ))
        shapes.append(cv.Text(
            cx - 10, cy + 10, "0",
            ft.TextStyle(size=10)
        ))
        
        # Draw tick marks and labels
        tick_paint = ft.Paint(color=ft.Colors.BLACK, stroke_width=1)
        
        # X-axis ticks
        for x in np.arange(-20, 21, 2):
            if x != 0:
                sx, sy = self.to_screen(x, 0)
                if 0 <= sx <= canvas_width:
                    shapes.append(cv.Line(sx, cy - 5, sx, cy + 5, tick_paint))
                    shapes.append(cv.Text(
                        sx - 5, cy + 10, str(int(x)),
                        ft.TextStyle(size=10)
                    ))
        
        # Y-axis ticks
        for y in np.arange(-20, 21, 2):
            if y != 0:
                sx, sy = self.to_screen(0, y)
                if 0 <= sy <= canvas_height:
                    shapes.append(cv.Line(cx - 5, sy, cx + 5, sy, tick_paint))
                    shapes.append(cv.Text(
                        cx - 20, sy + 5, str(int(y)),
                        ft.TextStyle(size=10)
                    ))
        
        # Draw the function curve
        self._draw_function(shapes, visible_x_min, visible_x_max, 
                           canvas_width, canvas_height)
        
        return shapes
    
    def _draw_function(self, shapes: List, x_min: float, x_max: float, 
                      canvas_width: float, canvas_height: float):
        """Draw the function curve"""
        try:
            curve_paint = ft.Paint(
                color=ft.Colors.RED,
                stroke_width=3,
                style=ft.PaintingStyle.STROKE
            )
            
            # Sample points
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = FunctionGraph.evaluate(self.state.expr, x_vals)
            
            # Create and add path
            path_elements = FunctionGraph.create_path(
                x_vals, y_vals, self.to_screen
            )
            
            if path_elements:
                shapes.append(cv.Path(path_elements, curve_paint))
        except Exception as e:
            print(f"Graph drawing error: {e}")
