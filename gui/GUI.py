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
                # Room 1 - Living Room (Main Room)
                {"id": 1, "height": 3.0, "width": 6.0, "position": [0, 0, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 2, "height": 3.0, "width": 6.0, "position": [0, 6, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 3, "height": 3.0, "width": 6.0, "position": [6, 0, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 4, "height": 3.0, "width": 6.0, "position": [0, 0, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Room 2 - Kitchen (connected to Living Room)
                {"id": 5, "height": 3.0, "width": 5.0, "position": [6, 0, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 6, "height": 3.0, "width": 5.0, "position": [6, 5, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 7, "height": 3.0, "width": 5.0, "position": [11, 0, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 8, "height": 3.0, "width": 5.0, "position": [6, 0, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Room 3 - Bedroom (connected to Living Room and Kitchen)
                {"id": 9, "height": 3.0, "width": 4.0, "position": [0, 6, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 10, "height": 3.0, "width": 4.0, "position": [0, 10, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 11, "height": 3.0, "width": 4.0, "position": [4, 6, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 12, "height": 3.0, "width": 4.0, "position": [0, 6, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Room 4 - Bathroom (connected to Bedroom)
                {"id": 13, "height": 3.0, "width": 3.0, "position": [4, 10, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 14, "height": 3.0, "width": 3.0, "position": [4, 13, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 15, "height": 3.0, "width": 3.0, "position": [7, 10, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 16, "height": 3.0, "width": 3.0, "position": [4, 10, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Room 5 - Dining Room (connected to Living Room and Kitchen)
                {"id": 17, "height": 3.0, "width": 5.0, "position": [6, 6, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 18, "height": 3.0, "width": 5.0, "position": [6, 11, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 19, "height": 3.0, "width": 5.0, "position": [11, 6, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 20, "height": 3.0, "width": 5.0, "position": [6, 6, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Room 6 - Hallway (connecting rooms together)
                {"id": 21, "height": 3.0, "width": 2.0, "position": [11, 0, 0], "orientation": "Vertical-x"},  # North Wall
                {"id": 22, "height": 3.0, "width": 2.0, "position": [11, 2, 0], "orientation": "Vertical-y"},  # East Wall
                {"id": 23, "height": 3.0, "width": 2.0, "position": [13, 0, 0], "orientation": "Vertical-x"},  # South Wall
                {"id": 24, "height": 3.0, "width": 2.0, "position": [11, 0, 0], "orientation": "Vertical-y"},  # West Wall
                
                # Closing missing walls to fully enclose the rooms:
                # 1. Connect the Hallway to Living Room
                {"id": 25, "height": 3.0, "width": 2.0, "position": [6, 0, 0], "orientation": "Vertical-x"},  # Wall between Living Room and Hallway
                
                # 2. Close off the Hallway and Dining Room
                {"id": 26, "height": 3.0, "width": 2.0, "position": [11, 5, 0], "orientation": "Vertical-y"},  # Wall between Dining Room and Hallway
                
                # 3. Close off the Kitchen and Hallway
                {"id": 27, "height": 3.0, "width": 2.0, "position": [11, 5, 0], "orientation": "Vertical-x"},  # Wall between Kitchen and Hallway
                
                # 4. Close off the Bedroom and Kitchen
                {"id": 28, "height": 3.0, "width": 4.0, "position": [6, 10, 0], "orientation": "Vertical-y"},  # Wall between Kitchen and Bedroom
                
                # 5. Close off Bathroom and Bedroom
                {"id": 29, "height": 3.0, "width": 4.0, "position": [4, 10, 0], "orientation": "Vertical-x"},  # Wall between Bedroom and Bathroom
                
                # Additional closing walls for complete enclosure
                {"id": 30, "height": 3.0, "width": 5.0, "position": [6, 11, 0], "orientation": "Vertical-x"},  # Wall between Hallway and Dining Room
                {"id": 31, "height": 3.0, "width": 2.0, "position": [11, 10, 0], "orientation": "Vertical-y"},  # Wall between Dining Room and Hallway
                {"id": 32, "height": 3.0, "width": 3.0, "position": [4, 6, 0], "orientation": "Vertical-y"},  # Wall between Bedroom and Living Room
                {"id": 33, "height": 3.0, "width": 2.0, "position": [11, 8, 0], "orientation": "Vertical-x"}   # Wall closing Dining Room and Kitchen
            ],
            "colors": ["White", "Yellow", "Blue", "Red", "Black"],
            "time_per_meter": 2.0,
            "max_time": 30000.0,
            "paint_availability": {
                "White": 15,
                "Yellow": 2000,
                "Blue": 150,
                "Black": 1005,
                "Red": 1000
            },
            "adjacency_constraint": True,
            "min_colors": 4,
            "start_position": [0, 0, 0]
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
        #self.setFixedSize(1000, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header Label
        Header = QLabel("Output Screen")
        Header.setObjectName("main_label_title2")
        Header.setAlignment(Qt.AlignCenter)  # Ensure label is centered
        layout.addWidget(Header)

        # Horizontal Box Layout for Details
        hbox = QHBoxLayout()

        # Time Section
        vbox_time_widget = QWidget()
        vbox_time = QVBoxLayout(vbox_time_widget)
        vbox_time_widget.setObjectName("vbox_sub")

        total_time_label = QLabel("Total Time")
        total_time_label.setObjectName("label_default")
        vbox_time.addWidget(total_time_label)

        total_time_value = QLabel(f"{float(solution['total_time'])}")
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

        colors_used_value = QLabel(f"{', '.join(list(set(solution['colors'])))}")
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

        paint_usage_value = QLabel(f"{solution['paint_usage']}")
        paint_usage_value.setObjectName("label_default2")
        vbox_paint_usage.addWidget(paint_usage_value)

        hbox.addWidget(vbox_paint_usage_widget)

        layout.addLayout(hbox)

        # Card-like Structure for 3D Plot
        plot_card_widget = QWidget()
        plot_card_widget.setObjectName("vbox_sub")  # Apply vbox_sub style to the container

        plot_card_layout = QVBoxLayout(plot_card_widget)
        plot_card_layout.setObjectName("vbox_sub")

        # Matplotlib 3D Plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        plot_card_layout.addWidget(self.canvas)

        layout.addWidget(plot_card_widget)

        # Render the 3D plot
        self.visualize_3d_environment(surfaces, solution["path"], solution["colors"])

    def visualize_3d_environment(self, surfaces, path, colors):
        """Visualizes the 3D environment using matplotlib."""
        self.figure.clear()  # Clear any previous plots

        # Create a 3D subplot with a transparent background
        ax = self.figure.add_subplot(111, projection="3d", facecolor=(0, 0, 0, 0))

        # Set the figure's background to transparent
        self.figure.patch.set_alpha(0)

        # Plot each wall with its assigned color
        for surface, color in zip(surfaces, colors):
            x, y, z = surface["position"]

            if surface["orientation"] == "Vertical-x":
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y, y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "Vertical-y":
                x_corners = [x, x, x, x]
                y_corners = [y, y + surface["width"], y + surface["width"], y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "horizontal":
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y + surface["height"], y + surface["height"]]
                z_corners = [z, z, z, z]

            vertices = [list(zip(x_corners, y_corners, z_corners))]
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, edgecolor=color, facecolors=color))

        # Plot traversal path
        if path:
            path_x, path_y, path_z = zip(*path)
            ax.plot(path_x, path_y, path_z, color="red", marker="o", label="Traversal Path")

        # Set labels and limits
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim([0, max(surface["position"][0] + surface["width"] for surface in surfaces) + 1])
        ax.set_ylim([0, max(surface["position"][1] + surface["height"] for surface in surfaces) + 1])
        ax.set_zlim([0, max(surface["position"][2] + surface["height"] for surface in surfaces) + 1])

        ax.set_title("3D Wall Painting Environment", alpha=0.8)
        ax.legend()

        # Update the canvas and make sure background is transparent
        self.canvas.setStyleSheet("background: transparent;")  # Ensure transparency in the canvas
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
        title_label = QLabel("Wall Painting Solver")
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
