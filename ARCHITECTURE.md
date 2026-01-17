## Flet Algebra - Code Structure

The application has been successfully refactored into a clean, modular architecture with separate files for different concerns.

### File Organization

```
src/
├── main.py              # Entry point - imports and runs the application
├── app.py               # GraphingApp class - orchestrates the UI
├── coordinate_system.py # CoordinateSystem class - handles graph rendering and interactions
├── models.py            # Data models and utility classes
└── assets/              # Resource directory
```

### Module Descriptions

#### `main.py` - Entry Point
- Clean entry point that initializes Flet and runs the application
- Imports `GraphingApp` from `app.py`
- Uses modern `ft.run()` instead of deprecated `ft.app()`

#### `app.py` - Application Class (244 lines)
- **GraphingApp class**: Main application orchestrator
  - `setup_page()`: Configures page properties (1200×800 window, white background)
  - `build_ui()`: Assembles the complete UI
  - `_create_drawer()`: Navigation drawer with menu items
  - `_create_top_bar()`: AppBar with title and buttons
  - `_create_controls_stack()`: Creates main content area with:
    - CoordinateSystem instance
    - Expression input field
    - Pan control buttons (up/down/left/right)
    - Zoom buttons (zoom in/out, reset)
    - Control panel with layout

#### `coordinate_system.py` - Graph Rendering (263 lines)
- **CoordinateSystem class**: Custom Flet composite control (extends `ft.Stack`)
  - `to_screen(x, y)`: Converts math coordinates to screen pixels
  - `_draw_graph()`: Renders complete graph including:
    - Major and minor grid lines
    - X and Y axes with arrows
    - Axis labels and tick marks
    - Mathematical function curve
  - Pan methods: `pan_up()`, `pan_down()`, `pan_left()`, `pan_right()`
  - Zoom methods: `zoom_in()`, `zoom_out()`, `reset_view()`
  - Event handlers: `_handle_pan_update()` (drag), `_handle_scroll()` (zoom)
  - `set_expression(expr)`: Updates the function to display
  - `redraw()`: Updates the canvas with new shapes
  - `did_mount()`: Lifecycle method - triggers initial draw when mounted

#### `models.py` - Data & Utilities (50 lines)
- **GraphState dataclass**: Manages application state
  - `scale`: Zoom level (default 50.0)
  - `offset_x`, `offset_y`: Pan offsets
  - `expr`: Current function expression (default "x**2")
  
- **FunctionGraph class**: Static utility methods
  - `evaluate(expr, x_vals)`: Safely evaluates math expressions
  - `create_path(x_vals, y_vals, to_screen_func)`: Generates canvas path elements

### Key Features

1. **Draggable Coordinate System**: Pan using mouse drag or buttons
2. **Zoom Control**: Zoom in/out with buttons or scroll wheel
3. **Function Graphing**: Enter expressions like `x**2`, `sin(x)`, `cos(x**2)`, etc.
4. **Grid & Axes**: Major/minor grid, labeled axes with arrows
5. **Responsive**: Window resize updates canvas
6. **Clean Architecture**: Separated concerns, reusable components

### Event Handling

- **Mouse Drag**: Calls `_handle_pan_update()` via GestureDetector
- **Scroll**: Calls `_handle_scroll()` for zoom
- **Button Clicks**: Trigger pan/zoom/reset methods
- **Text Change**: Updates expression and triggers redraw

### Coordinate Transformation

- Math coords (x, y) → Screen coords (sx, sy)
- Origin at screen center
- Y-axis inverted (math up = screen up)
- Scale in pixels per unit

### Deprecation Fixes

- Updated from `ft.app()` to `ft.run()`
- Updated from `page.window_width` to `page.window.width`
- Updated drag events from `delta_x/delta_y` to `local_delta.x/y`
- Removed deprecated ref handling for Canvas

### Running the Application

```bash
cd src
python main.py
```

The application opens at 1200×800 pixels with a white background and displays a Cartesian coordinate system with the default function y=x² plotted in red.
