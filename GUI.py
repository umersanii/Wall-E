from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
import sys

class StylishApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 with CSS")
        self.setGeometry(200, 200, 400, 300)

        # Set a layout
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("Enter your name:")
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        # Add a text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type here...")
        layout.addWidget(self.text_input)

        # Add a button
        button = QPushButton("Submit")
        button.clicked.connect(self.on_submit)
        layout.addWidget(button)

        # Set the layout to the main window
        self.setLayout(layout)

    def on_submit(self):
        name = self.text_input.text()
        if name:
            print(f"Hello, {name}!")
        else:
            print("Please enter your name.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load styles from an external file
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())

    window = StylishApp()
    window.show()

    sys.exit(app.exec_())