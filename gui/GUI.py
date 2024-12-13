from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QSpinBox, QComboBox, QMessageBox, QScrollArea, QGroupBox, QHBoxLayout, QFileDialog
import sys
from PyQt5.QtCore import Qt
import json
from processing.WallE import WallE

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WALL-E!")
        self.setGeometry(550, 300, 600, 500)
        self.setFixedSize(600, 500)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setObjectName("main_layout")

        # Welcome screen components
        self.welcome_label = QLabel("WALL-E!")
        self.welcome_label.setObjectName("main_label_title")
        self.layout.addWidget(self.welcome_label)

        # Buttons for different input methods
        button_layout = QVBoxLayout()
        button_layout.setObjectName("button_layout_container")

        self.manual_button = QPushButton("Enter Input Manually")
        self.manual_button.setObjectName("button_main_menu")
        self.manual_button.clicked.connect(self.show_manual_input)
        button_layout.addWidget(self.manual_button)

        self.load_button = QPushButton("Load JSON File")
        self.load_button.setObjectName("button_main_menu")
        self.load_button.clicked.connect(self.load_json_file)
        button_layout.addWidget(self.load_button)

        self.test_button = QPushButton("Test Sample JSON")
        self.test_button.setObjectName("button_main_menu")
        self.test_button.clicked.connect(self.load_test_sample)
        button_layout.addWidget(self.test_button)

        self.layout.addLayout(button_layout)

        # Set the layout for the window
        self.setLayout(self.layout)

    def show_manual_input(self):
        """Switch to manual input screen."""
        self.manual_input_screen = ManualInputScreen()
        self.manual_input_screen.show()
        self.close()

    def show_output_screen(self):
        """Switch to manual input screen."""
        self.output_screen = OutputScreen()
        self.output_screen.show()
        self.close()

    def load_json_file(self):
        """Allow the user to load a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r") as file:
                    data = json.load(file)
                    Walle = WallE(data)
                    Walle.display_solutions(Walle.solve())

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load JSON file: {e}")

    def load_test_sample(self):
        """Load a predefined sample JSON."""
        sample_data = {
            "surfaces": [
                # Room 1 walls
                {"id": 1, "height": 3, "width": 6, "position": [0, 0, 0], "orientation": "Vertical-x"},  # Wall 1 (Room 1)
                {"id": 2, "height": 3, "width": 6, "position": [0, 6, 0], "orientation": "Vertical-x"},  # Wall 2 (Room 1)
                {"id": 3, "height": 3, "width": 6, "position": [6, 0, 0], "orientation": "Vertical-y"},  # Wall 3 (Room 1)
                {"id": 4, "height": 3, "width": 6, "position": [0, 0, 0], "orientation": "Vertical-y"},  # Wall 4 (Room 1)
                {"id": 15, "height": 6, "width": 6, "position": [0, 0, 3], "orientation": "horizontal"},  # Ceiling (Room 1)
                
                # Room 3 walls (sharing 3 walls with Room 2)
                {"id": 9, "height": 3, "width": 8, "position": [6, 0, 0], "orientation": "Vertical-x"},  # Wall 1 (Room 3) - shared with Room 2
                {"id": 10, "height": 3, "width": 8, "position": [6, 6, 0], "orientation": "Vertical-x"},  # Wall 2 (Room 3) - shared with Room 2
                {"id": 11, "height": 3, "width": 6, "position": [14, 0, 0], "orientation": "Vertical-y"},  # Wall 3 (Room 3) - shared with Room 2
                {"id": 12, "height": 3, "width": 8, "position": [6, 6, 0], "orientation": "Vertical-y"},  # Duplicate shared wall (adjust logic later if needed)
                {"id": 13, "height": 3, "width": 8, "position": [0, 6, 0], "orientation": "Vertical-y"},  # Wall between Room 1 and Room 2
                {"id": 14, "height": 3, "width": 6, "position": [0, 14, 0], "orientation": "Vertical-x"},  # Wall connecting Room 1 and Room 3
            ],
            "colors": ["Red", "Yellow", "Blue", "White", "Black"],
            "time_per_meter": 2.0,
            "max_time": 30000.0,
            "paint_availability": {
                "White": 150,
                "Yellow": 2000,
                "Blue": 150,
                "Black": 1005,
                "Red": 1000
            },
            "adjacency_constraint": True,
            "min_colors": 4,
            "start_position": [0, 0, 0],
            "doors": {
                # Door specifications for shared walls
                9: {"door_position": [6, 4, 0]},  # Door in Wall 9
                10: {"door_position": [6, 9, 0]},  # Door in Wall 10
                11: {"door_position": [14, 3, 0]},  # Door in Wall 11
                13: {"door_position": [0, 9, 0]},  # Door in Wall 13
            }
        }

        Walle = WallE(sample_data)
        solution = Walle.solve()
        #Walle.display_solutions()
        self.output_screen = OutputScreen(solution, sample_data["surfaces"])
        self.output_screen.show()
        self.close()

    def load_data_to_manual_input(self, data):
        """Load the JSON data into the manual input screen."""
        self.manual_input_screen = ManualInputScreen(data)
        self.manual_input_screen.show()
        self.close()



class OutputScreen(QWidget):
    def __init__(self, solution, surfaces):
        super().__init__()
        self.setWindowTitle("Output Screen")
        self.setGeometry(200, 200, 600, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header Label
        Header = QLabel("Output Screen")
        Header.setObjectName("main_label_title2")
        Header.setAlignment(Qt.AlignCenter)  # Ensure label is centered
        layout.addWidget(Header)

        # Check if solution is None
        if solution is None:
            # Display "Solution Not Found"
            error_label = QLabel("Solution Not Found")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

            # Skip further processing (no need to display time, colors, or 3D plot)
            return

        # Horizontal Box Layout for Details
        hbox = QHBoxLayout()

        # Time Section
        vbox_time_widget = QWidget()
        vbox_time = QVBoxLayout(vbox_time_widget)
        vbox_time_widget.setObjectName("vbox_sub")

        total_time_label = QLabel("Total Time")
        total_time_label.setObjectName("label_default")
        vbox_time.addWidget(total_time_label)

        if solution['total_time'] is not None:
            total_time_value = QLabel(f"{int(solution['total_time'])}")
        else:
            total_time_value = QLabel("NAN")

        total_time_value.setAlignment(Qt.AlignCenter)
        total_time_value.setObjectName("label_default2")
        vbox_time.addWidget(total_time_value)

        hbox.addWidget(vbox_time_widget)

        # Colors Section
        vbox_colors_widget = QWidget()
        vbox_colors = QVBoxLayout(vbox_colors_widget)
        vbox_colors_widget.setObjectName("vbox_sub")
        
        colors_used_label = QLabel("Colors Used")
        colors_used_label.setObjectName("label_default")
        vbox_colors.addWidget(colors_used_label)
        
        if 'colors' in solution and isinstance(solution['colors'], dict):
            unique_colors = set(solution['colors'].values())
            colors_used_value = QLabel(f"{', '.join(unique_colors)}")
        else:
            colors_used_value = QLabel("NAN")

        colors_used_value.setAlignment(Qt.AlignCenter)
        colors_used_value.setObjectName("label_default2")
        vbox_colors.addWidget(colors_used_value)
        
        hbox.addWidget(vbox_colors_widget)

        # Paint Usage Section
        vbox_paint_usage_widget = QWidget()
        vbox_paint_usage = QVBoxLayout(vbox_paint_usage_widget)
        vbox_paint_usage_widget.setObjectName("vbox_sub")
        
        paint_usage_label = QLabel("Paint Usage")
        paint_usage_label.setObjectName("label_default")
        vbox_paint_usage.addWidget(paint_usage_label)
        
        if solution and 'paint_usage' in solution and isinstance(solution['paint_usage'], dict):
            paint_usage = solution['paint_usage']
            paint_usage_values = [paint_usage[color] for color in unique_colors if color in paint_usage]
            paint_usage_values_str = ', '.join(map(str, paint_usage_values))
            paint_usage_value = QLabel(f"{paint_usage_values_str}")
        else:
            paint_usage_value = QLabel("NAN")
        
        paint_usage_value.setObjectName("label_default2")
        vbox_paint_usage.addWidget(paint_usage_value)
        
        hbox.addWidget(vbox_paint_usage_widget)
        layout.addLayout(hbox)

        # Card-like Structure for 3D Plot
        plot_card_widget = QWidget()
        plot_card_widget.setObjectName("vbox_sub")

        plot_card_layout = QVBoxLayout(plot_card_widget)
        plot_card_layout.setObjectName("vbox_sub")

        # Matplotlib 3D Plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        plot_card_layout.addWidget(self.canvas)

        layout.addWidget(plot_card_widget)

        # Render the 3D plot
        if solution is not None:
            self.visualize_3d_environment(surfaces, solution["path"], solution["colors"])
        else:
            # If no solution, do not render the 3D plot
            print("No solution to display 3D plot.")
    
    def visualize_3d_environment(self, surfaces, path, colors):
        """Visualizes the 3D environment using matplotlib."""
        self.figure.clear()  # Clear any previous plots

        # Create a 3D subplot with a transparent background
        ax = self.figure.add_subplot(111, projection="3d", facecolor=(0, 0, 0, 0))
        self.figure.patch.set_alpha(0)  # Set the figure's background to transparent

        # Validate and map colors
        if isinstance(colors, dict):
            # Map colors based on surface IDs
            mapped_colors = [colors.get(surface["id"], "gray") for surface in surfaces]
        else:
            # Assume colors is already a list
            mapped_colors = colors

        # Plot each wall with its assigned color
        for surface, color in zip(surfaces, mapped_colors):
            x, y, z = surface["position"]
            width = surface["width"]
            height = surface["height"]
            orientation = surface["orientation"]

            # Compute the vertices based on the wall orientation
            if orientation == "Vertical-x":
                # Wall is aligned with the X-axis (height on Z-axis)
                x_corners = [x, x + width, x + width, x]
                y_corners = [y, y, y, y]
                z_corners = [z, z, z + height, z + height]
            elif orientation == "Vertical-y":
                # Wall is aligned with the Y-axis (height on Z-axis)
                x_corners = [x, x, x, x]
                y_corners = [y, y + width, y + width, y]
                z_corners = [z, z, z + height, z + height]
            elif orientation == "horizontal":
                # Wall is horizontal (height on Z-axis)
                x_corners = [x, x + width, x + width, x]
                y_corners = [y, y, y + height, y + height]
                z_corners = [z, z, z, z]
            else:
                raise ValueError(f"Invalid orientation '{orientation}' for surface ID {surface['id']}.")

            # Debugging: Print out the vertices and their positions
            print(f"Surface {surface['id']} corners: {list(zip(x_corners, y_corners, z_corners))}")

            # Create vertices list and add the wall to the 3D plot
            vertices = [list(zip(x_corners, y_corners, z_corners))]

            # Plot the surface (wall) with edge colors and transparency
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, edgecolor='black', facecolors=color))

        # Plot traversal path if provided
        if path:
            try:
                # Ensure path is valid (list of tuples of (x, y, z) coordinates)
                path_x, path_y, path_z = zip(*path)
                ax.plot(path_x, path_y, path_z, color="red", marker="o", label="Traversal Path")
            except ValueError:
                raise ValueError("Path must be a list of tuples/lists with three numeric values each (x, y, z).")

        # Set labels and limits
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Calculate the limits of the plot based on surfaces
        max_x = max(surface["position"][0] + surface.get("width", 0) for surface in surfaces) + 1
        max_y = max(surface["position"][1] + surface.get("width", 0) for surface in surfaces) + 1
        max_z = max(surface["position"][2] + surface.get("height", 0) for surface in surfaces) + 1

        ax.set_xlim([0, max_x])
        ax.set_ylim([0, max_y])
        ax.set_zlim([0, max_z])

        ax.set_title("3D Wall Painting Environment", alpha=0.8)
        ax.legend()

        # Update the canvas and set its style
        self.canvas.setStyleSheet("background: transparent;")
        self.canvas.draw()

class ManualInputScreen(QWidget):
    def __init__(self, data=None):
        super().__init__()

        self.setWindowTitle("Wall Painting Solver")
        self.setGeometry(200, 200, 600, 500)

        # Main layout
        layout = QVBoxLayout()
        layout.setObjectName("main_layout")

        # Title label
        title_label = QLabel("Wall E")
        title_label.setObjectName("main_label_title2")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Wall count
        label_wall_count = QLabel("Number of Walls")
        label_wall_count.setObjectName("label_default")
        self.wall_count = QSpinBox()
        self.wall_count.setMinimum(1)
        self.wall_count.setMaximum(20)
        self.wall_count.valueChanged.connect(self.update_wall_inputs)
        form_layout.addRow(label_wall_count, self.wall_count)

        # Wall inputs in scroll area
        self.wall_group_box = QGroupBox("Wall Inputs")
        self.wall_group_box.setObjectName("wall_group_box")
        self.wall_layout = QFormLayout()
        self.wall_group_box.setLayout(self.wall_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.wall_group_box)
        form_layout.addRow(self.scroll_area)

        # Additional inputs
        label_colors = QLabel("Available Colors")
        label_colors.setObjectName("label_default")
        self.colors_input = QLineEdit()
        self.colors_input.setPlaceholderText("Enter available colors (comma-separated)...")
        self.colors_input.setObjectName("colors_input")
        form_layout.addRow(label_colors, self.colors_input)

        label_time = QLabel("Time per Square Meter")
        label_time.setObjectName("label_default")
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter time per square meter (e.g., 2.0)...")
        self.time_input.setObjectName("time_input")
        form_layout.addRow(label_time, self.time_input)

        label_max_time = QLabel("Max Time")
        label_max_time.setObjectName("label_default")
        self.max_time_input = QLineEdit()
        self.max_time_input.setPlaceholderText("Enter max allowed time (e.g., 30000)...")
        self.max_time_input.setObjectName("max_time_input")
        form_layout.addRow(label_max_time, self.max_time_input)

        label_min_colors = QLabel("Minimum Distinct Colors")
        label_min_colors.setObjectName("label_default")
        self.min_colors_input = QLineEdit()
        self.min_colors_input.setPlaceholderText("Enter minimum distinct colors (e.g., 3)...")
        self.min_colors_input.setObjectName("min_colors_input")
        form_layout.addRow(label_min_colors, self.min_colors_input)

        label_start_position = QLabel("Start Position")
        label_start_position.setObjectName("label_default")
        self.start_position_input = QLineEdit()
        self.start_position_input.setPlaceholderText("Enter start position (x,y,z)...")
        self.start_position_input.setObjectName("start_position_input")
        form_layout.addRow(label_start_position, self.start_position_input)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.setObjectName("submit_button")
        submit_button.clicked.connect(self.on_submit)
        form_layout.addRow(submit_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)
        self.update_wall_inputs()

    def update_wall_inputs(self):
        """Update wall inputs dynamically based on wall count."""
        for i in reversed(range(self.wall_layout.count())):
            widget = self.wall_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.wall_inputs = []
        for i in range(self.wall_count.value()):
            height_input = QLineEdit()
            height_input.setPlaceholderText(f"Height of Wall {i + 1}")
            width_input = QLineEdit()
            width_input.setPlaceholderText(f"Width of Wall {i + 1}")
            position_input = QLineEdit()
            position_input.setPlaceholderText(f"Position of Wall {i + 1} (x,y,z)")
            orientation_input = QComboBox()
            orientation_input.addItems(["Vertical-x", "Vertical-y", "Horizontal"])

            self.wall_layout.addRow(f"Wall {i + 1} Height", height_input)
            self.wall_layout.addRow(f"Wall {i + 1} Width", width_input)
            self.wall_layout.addRow(f"Wall {i + 1} Position", position_input)
            self.wall_layout.addRow(f"Wall {i + 1} Orientation", orientation_input)

            self.wall_inputs.append({
                "height": height_input,
                "width": width_input,
                "position": position_input,
                "orientation": orientation_input,
            })

    def get_wall_data(self):
        wall_data = []
        for i, wall_input in enumerate(self.wall_inputs):
                try:
                    height = float(wall_input["height"].text())
                    width = float(wall_input["width"].text())
                    position = list(map(float, wall_input["position"].text().split(",")))
                    orientation = wall_input["orientation"].currentText()
                    wall_data.append({
                        "id": i + 1,  # Assign a unique id starting from 1
                        "height": height,
                        "width": width,
                        "position": position,
                        "orientation": orientation
                    })
                except ValueError:
                    QMessageBox.critical(self, "Input Error", "Please ensure all wall fields are filled correctly.")
                    return None
        return wall_data

    def on_submit(self):
        surfaces = self.get_wall_data()
        if surfaces is None:  # Validation failed
            return

        try:
            data = {
                "surfaces": surfaces,
                "colors": [color.strip() for color in self.colors_input.text().split(",") if color.strip()],
                "time_per_meter": float(self.time_input.text()),
                "max_time": float(self.max_time_input.text()),
                "min_colors": int(self.min_colors_input.text()),
                "start_position": list(map(float, self.start_position_input.text().split(","))),
            }
            print(data)
            WallE_obj = WallE(data)
            WallE_obj.display_solutions(WallE_obj.solve())
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please ensure all inputs are correctly formatted.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load styles from an external file
    try:
        with open("styles.css", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Warning: styles.css not found. Using default styles.")

    window = App()
    window.show()
    sys.exit(app.exec_())
