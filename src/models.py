"""Data models and utility classes for the graphing application"""

import numpy as np
import flet.canvas as cv
from dataclasses import dataclass, field
from typing import List


@dataclass
class GraphState:
    """State management for the graph"""
    scale: float = 50.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    expr: str = "x**2"
    expressions: List[str] = field(default_factory=lambda: ["x**2"])  # Support multiple functions
    show_minor_grid: bool = True


class FunctionGraph:
    """Utility class for evaluating and drawing mathematical functions"""
    
    @staticmethod
    def evaluate(expr: str, x_vals: np.ndarray) -> np.ndarray:
        """Safely evaluate a mathematical expression"""
        y_vals = []
        for x in x_vals:
            try:
                y = eval(expr, {"x": x, "np": np, "__builtins__": {}})
                y_vals.append(y)
            except:
                y_vals.append(float('nan'))
        return np.array(y_vals)
    
    @staticmethod
    def create_path(x_vals: np.ndarray, y_vals: np.ndarray, 
                   to_screen_func) -> List:
        """Create path elements for drawing the curve"""
        path_elements = []
        first_valid = True
        
        for i in range(len(x_vals)):
            if not np.isnan(y_vals[i]):
                sx, sy = to_screen_func(x_vals[i], y_vals[i])
                if first_valid:
                    path_elements.append(cv.Path.MoveTo(sx, sy))
                    first_valid = False
                else:
                    path_elements.append(cv.Path.LineTo(sx, sy))
        
        return path_elements
