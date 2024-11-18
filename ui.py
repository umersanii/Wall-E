import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

class WallPaintingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wall Painting Solver")
        self.root.geometry("800x600")
        self.root.configure(bg="#F0F0F0")

        # Variables for wall input
        self.wall_entries = []  # To store entries for dimensions
        self.color_vars = []  # To store selected colors
        self.time_per_meter = tk.DoubleVar(value=2.0)  # Default time per square meter
        self.test_mode = tk.BooleanVar(value=False)  # Test mode toggle

        self.create_widgets()

    def create_widgets(self):
        """Sets up widgets for wall dimensions, colors, and time system."""
        ttk.Label(self.root, text="Wall Painting Solver", font=("Arial", 18), background="#F0F0F0").grid(
            row=0, column=0, columnspan=3, pady=10
        )

        # Wall dimensions input
        ttk.Label(self.root, text="Enter Wall Dimensions (Height × Width):").grid(
            row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5
        )

        for i in range(4):  # Assume 4 walls for simplicity
            frame = ttk.Frame(self.root)
            frame.grid(row=2 + i, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
            ttk.Label(frame, text=f"Wall {i+1}:").grid(row=0, column=0, padx=5)
            entry_height = ttk.Entry(frame, width=10)
            entry_height.grid(row=0, column=1, padx=5)
            ttk.Label(frame, text="×").grid(row=0, column=2)
            entry_width = ttk.Entry(frame, width=10)
            entry_width.grid(row=0, column=3, padx=5)
            self.wall_entries.append((entry_height, entry_width))

            # Color picker for each wall
            color_var = tk.StringVar(value="#FFFFFF")
            self.color_vars.append(color_var)
            color_button = tk.Button(
                frame,
                text="Select Color",
                bg=color_var.get(),
            )
            
            color_button.grid(row=0, column=4, padx=10)

        # Time per square meter input
        ttk.Label(self.root, text="Time Per Square Meter (minutes):").grid(
            row=7, column=0, sticky=tk.W, padx=10, pady=10
        )
        ttk.Entry(self.root, textvariable=self.time_per_meter, width=10).grid(row=7, column=1, padx=10)

        # Test mode toggle
        ttk.Checkbutton(self.root, text="Enable Test Mode", variable=self.test_mode, command=self.fill_test_data).grid(
            row=8, column=0, sticky=tk.W, padx=10, pady=10
        )

        # Solve button
        solve_button = ttk.Button(self.root, text="Solve", command=self.solve_csp)
        solve_button.grid(row=9, column=0, columnspan=3, pady=20)

    def pick_color(self, color_var, button):
        """Allows users to select a color."""
        color_code = colorchooser.askcolor(title="Choose Wall Color")[1]
        if color_code:
            color_var.set(color_code)
            button.configure(bg=color_code)

    def fill_test_data(self):
        """Fills in test data if test mode is enabled."""
        if self.test_mode.get():
            # Predefined test data
            test_dimensions = [(2.5, 3.0), (2.0, 2.5), (3.0, 2.0), (2.5, 2.5)]  # (Height, Width)
            test_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]  # RGB Colors
            for i, (entry_height, entry_width) in enumerate(self.wall_entries):
                entry_height.delete(0, tk.END)
                entry_height.insert(0, test_dimensions[i][0])
                entry_width.delete(0, tk.END)
                entry_width.insert(0, test_dimensions[i][1])
                self.color_vars[i].set(test_colors[i])
        else:
            # Clear test data when disabled
            for entry_height, entry_width in self.wall_entries:
                entry_height.delete(0, tk.END)
                entry_width.delete(0, tk.END)
            for color_var in self.color_vars:
                color_var.set("#FFFFFF")

    def solve_csp(self):
        """Solves the CSP and calculates the time."""
        walls = []
        for i, (entry_height, entry_width) in enumerate(self.wall_entries):
            try:
                height = float(entry_height.get())
                width = float(entry_width.get())
                area = height * width
                color = self.color_vars[i].get()
                walls.append({"area": area, "color": color})
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter valid dimensions for Wall {i+1}.")
                return

        time_per_meter = self.time_per_meter.get()

        # Calculate total painting time
        total_time = sum(wall["area"] * time_per_meter for wall in walls)

        # Show result
        result_text = f"Total Painting Time: {total_time:.2f} minutes\n"
        for i, wall in enumerate(walls, start=1):
            result_text += f"Wall {i}: Area={wall['area']:.2f} sq. meters, Color={wall['color']}\n"

        messagebox.showinfo("Solution", result_text)

    def run(self):
        """Runs the application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = WallPaintingApp()
    app.run()
