"""
Flet Algebra - GeoGebra-like Algebra Equation Drawing Program

PROJECT STRUCTURE:
==================

This project demonstrates a modern Python application using the Flet framework
to create an interactive graphing calculator. It follows OOP principles with
separation of concerns.

FILE BREAKDOWN:
===============

1. main.py (YOU ARE HERE)
   - Entry point of the application
   - Creates the Flet page and initializes the GraphingApp
   - Runs the application using ft.run()
   - This is the simplest file - just starts everything

2. graphing_app.py
   - Main application class: GraphingApp
   - Handles UI orchestration (AppBar, Drawer, BottomAppBar, Control Panel)
   - Manages user interactions (button clicks, menu selections)
   - Coordinates between the UI and the coordinate system
   - Contains methods for pan/zoom/reset operations
   - This is where the "big picture" UI logic lives

3. coordinate_system.py
   - Custom composite control: CoordinateSystem (extends ft.Stack)
   - Handles all canvas-based drawing (grid, axes, labels, function curves)
   - Manages mouse interactions (drag to pan, scroll to zoom)
   - Contains the mathematical coordinate transformation logic
   - This is where the "drawing" happens

4. graph_state.py
   - Data models: GraphState (dataclass) and FunctionGraph (utility class)
   - GraphState stores all application state (scale, offset, expressions, etc.)
   - FunctionGraph provides math utilities (evaluate expressions, create paths)
   - This is where the "data" and "math" logic lives

HOW IT WORKS:
=============

1. User runs: python main.py
2. main.py creates a Flet Page and GraphingApp
3. GraphingApp builds the UI (AppBar, Drawer, Control Panel, Coordinate System)
4. CoordinateSystem creates a Canvas and sets up gesture detectors
5. User interacts:
   - Types function in text field → added to expressions list
   - Clicks Submit → function is drawn on canvas
   - Drags mouse → pan the view
   - Scrolls wheel → zoom in/out
   - Clicks menu items → toggle grid, dark mode, reset view
6. All state is stored in GraphState dataclass
7. Canvas redraws when state changes

KEY FEATURES:
=============
- Multiple function graphing with different colors
- Pan and zoom with mouse
- Toggleable minor grid
- Dark mode / Day mode toggle
- Dynamic axis labels (adjusts based on zoom level)
- Responsive UI with bottom app bar (on long-press)
- Navigation drawer for future features

LEARNING PATH:
==============
1. Start with main.py (simplest)
2. Read graphing_app.py to understand UI structure
3. Study coordinate_system.py for drawing logic
4. Examine graph_state.py for data models
5. Experiment by modifying colors, adding features

"""

import flet as ft
from graphing_app import GraphingApp


def main(page: ft.Page):
    """Main entry point"""
    app = GraphingApp(page)
    app.build_ui()


if __name__ == "__main__":
    ft.run(main)
