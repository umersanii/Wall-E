from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QSpinBox, QComboBox, QMessageBox, QScrollArea, QGroupBox, QHBoxLayout, QFileDialog
import sys
from PyQt5.QtCore import Qt
import json
from processing.WallE import WallE


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
                {"id": 1, "height": 3.0, "width": 4.0, "position": [0, 0, 0], "orientation": "vertical-x"},
                {"id": 2, "height": 3.0, "width": 4.0, "position": [4, 0, 0], "orientation": "vertical-y"}
            ],
            "colors": ["White", "Yellow", "Blue"],
            "time_per_meter": 2.0,
            "max_time": 30000.0,
            "paint_availability": {
                "White": 15,
                "Yellow": 2000,
                "Blue": 1500,
                "Black": 1005,
                "Red": 1000
            },
            "adjacency_constraint": True,
            "min_colors": 3,
            "start_position": [0, 0, 0]
        }
        self.load_data_to_manual_input(sample_data)

    def load_data_to_manual_input(self, data):
        """Load the JSON data into the manual input screen."""
        self.manual_input_screen = ManualInputScreen(data)
        self.manual_input_screen.show()
        self.close()


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
