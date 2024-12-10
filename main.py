from PyQt5.QtWidgets import QApplication
import sys
from gui.GUI import App
if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("resources\styles.css", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Warning: styles.css not found. Using default styles.")

    window = App()
    window.show()
    sys.exit(app.exec_())
