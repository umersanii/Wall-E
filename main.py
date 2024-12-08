import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from itertools import product
import random
import matplotlib.pyplot as plt
import numpy as np


class WallPaintingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wall Painting Solver")
        self.root.geometry("800x700")
        self.root.configure(bg="#F0F0F0")

        # Variables for wall and roof input
        self.surface_entries = []  # To store entries for dimensions (walls and roof)
        self.color_vars = []  # To store selected colors
        self.time_per_meter = tk.DoubleVar(value=2.0)  # Default time per square meter
        self.max_time = tk.DoubleVar(value=100.0)  # Max allowed painting time
        self.test_mode = tk.BooleanVar(value=False)  # Test mode toggle

        self.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFFFFF"]  # Predefined colors
        self.valid_solutions = []  # Store valid solutions

        # Tab setup
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.setup_input_tab()
        self.setup_visualization_tab()
        self.setup_metrics_tab()

    def setup_input_tab(self):
        """Sets up the input tab for surface dimensions and constraints."""
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Input")

        ttk.Label(self.input_tab, text="Wall and Roof Painting Solver", font=("Arial", 18)).grid(
            row=0, column=0, columnspan=3, pady=10
        )

        # Surface dimensions input (walls and roof)
        ttk.Label(self.input_tab, text="Enter Dimensions (Height × Width):").grid(
            row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5
        )

        for i in range(5):  # Assume 4 walls and 1 roof for simplicity
            frame = ttk.Frame(self.input_tab)
            frame.grid(row=2 + i, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
            ttk.Label(frame, text=f"Surface {i+1}:").grid(row=0, column=0, padx=5)
            entry_height = ttk.Entry(frame, width=10)
            entry_height.grid(row=0, column=1, padx=5)
            ttk.Label(frame, text="×").grid(row=0, column=2)
            entry_width = ttk.Entry(frame, width=10)
            entry_width.grid(row=0, column=3, padx=5)
            self.surface_entries.append((entry_height, entry_width))

        # Time per square meter input
        ttk.Label(self.input_tab, text="Time Per Square Meter (minutes):").grid(
            row=7, column=0, sticky=tk.W, padx=10, pady=5
        )
        ttk.Entry(self.input_tab, textvariable=self.time_per_meter, width=10).grid(row=7, column=1, padx=10)

        # Max time input
        ttk.Label(self.input_tab, text="Max Allowed Time (minutes):").grid(
            row=8, column=0, sticky=tk.W, padx=10, pady=5
        )
        ttk.Entry(self.input_tab, textvariable=self.max_time, width=10).grid(row=8, column=1, padx=10)

        # Test mode toggle
        ttk.Checkbutton(self.input_tab, text="Enable Test Mode", variable=self.test_mode, command=self.fill_test_data).grid(
            row=9, column=0, sticky=tk.W, padx=10, pady=10
        )

        # Solve button
        solve_button = ttk.Button(self.input_tab, text="Solve", command=self.solve_csp)
        solve_button.grid(row=10, column=0, columnspan=3, pady=20)

    def setup_visualization_tab(self):
        """Sets up the visualization tab."""
        self.visualization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_tab, text="Visualization")

        self.canvas = tk.Canvas(self.visualization_tab, bg="#FFFFFF", width=600, height=400)
        self.canvas.pack(pady=20)

    def setup_metrics_tab(self):
        """Sets up the metrics tab."""
        self.metrics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.metrics_tab, text="Metrics Report")

        ttk.Label(self.metrics_tab, text="Metrics Report", font=("Arial", 18)).pack(pady=10)

        self.metrics_tree = ttk.Treeview(self.metrics_tab, columns=("Colors", "Time"), show="headings")
        self.metrics_tree.heading("Colors", text="Colors")
        self.metrics_tree.heading("Time", text="Time (minutes)")
        self.metrics_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def fill_test_data(self):
        """Fills in test data if test mode is enabled."""
        if self.test_mode.get():
            # Predefined test data
            test_dimensions = [(2.5, 3.0), (2.0, 2.5), (3.0, 2.0), (2.5, 2.5), (2.0, 3.0)]  # (Height, Width)
            for i, (entry_height, entry_width) in enumerate(self.surface_entries):
                entry_height.delete(0, tk.END)
                entry_height.insert(0, test_dimensions[i][0])
                entry_width.delete(0, tk.END)
                entry_width.insert(0, test_dimensions[i][1])
        else:
            # Clear test data when disabled
            for entry_height, entry_width in self.surface_entries:
                entry_height.delete(0, tk.END)
                entry_width.delete(0, tk.END)

    def solve_csp(self):
        """Solves the CSP and calculates all valid solutions."""
        surfaces = []
        for i, (entry_height, entry_width) in enumerate(self.surface_entries):
            try:
                height = float(entry_height.get())
                width = float(entry_width.get())
                area = height * width
                # Store the dimensions and area in a dictionary for each surface
                surfaces.append({"area": area, "height": height, "width": width})
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter valid dimensions for Surface {i+1}.")
                return

        time_per_meter = self.time_per_meter.get()
        max_allowed_time = self.max_time.get()

        # Generate all possible color combinations (This will generate multiple possible combinations)
        color_combinations = list(product(self.colors, repeat=len(surfaces)))

        # Filter combinations that satisfy constraints
        self.valid_solutions = []
        for combination in color_combinations:
            total_time = 0
            for i, (surface, color) in enumerate(zip(surfaces, combination)):
                total_time += surface["area"] * time_per_meter
                # Agent behavior: if adjacent surfaces have the same color, it's quicker
                if i > 0 and combination[i] == combination[i - 1]:
                    total_time -= 1  # Reduce time if adjacent surfaces have the same color

            # Check total time constraint
            if total_time > max_allowed_time:
                continue

            # New constraint: Wall size constraints (e.g., surface area should be within a specific range)
            if any(surface["area"] < 5 or surface["area"] > 30 for surface, color in zip(surfaces, combination)):
                continue

            # New constraint: Color Availability (ensure that a certain number of colors are used)
            if len(set(combination)) < 3:  # Require at least 3 distinct colors
                continue

            # New constraint: Surface Proportions (height to width ratio should be between 0.5 and 2.0)
            if any(0.5 > surface["height"] / surface["width"] or surface["height"] / surface["width"] > 2.0 for surface in surfaces):
                continue

            self.valid_solutions.append({
                "colors": combination, 
                "time": total_time,
                "surfaces": surfaces  # Include surfaces data
            })

        # Sort solutions by time and select the top 10 solutions
        self.valid_solutions.sort(key=lambda x: x["time"])
        self.valid_solutions = self.valid_solutions[:10]

        # Show results
        if self.valid_solutions:
            self.visualize_solutions(self.valid_solutions)  # Visualize the top 10 solutions
            self.populate_metrics()  # Populate metrics report
            messagebox.showinfo("Solutions", f"Found {len(self.valid_solutions)} valid solutions.")
        else:
            messagebox.showinfo("No Solutions", "No valid solutions found within the constraints.")

    
    def visualize_solutions(self, solutions):
        """Visualizes the top solutions with bar plots for each solution."""
        self.canvas.delete("all")  # Clear canvas

        x_offset = 50  # Set an initial offset for the x-axis
        for solution_index, solution in enumerate(solutions):
            y_offset = solution_index * 50 + 10  # Vertical offset for each solution
            for j, (color, surface) in enumerate(zip(solution["colors"], solution["surfaces"])):

                # Get the width and height of the surface
                width = surface["width"]
                height = surface["height"]

                self.canvas.create_rectangle(
                    x_offset + j * 100, y_offset, x_offset + j * 100 + 50, y_offset + 30,
                    fill=color
                )
                self.canvas.create_text(
                    x_offset + j * 100 + 25, y_offset + 15, text=f"{solution['time']:.2f}", fill="black"
                )


    def populate_metrics(self):
        """Populates the metrics tab with the valid solutions."""
        for row in self.metrics_tree.get_children():
            self.metrics_tree.delete(row)

        for solution in self.valid_solutions:
            self.metrics_tree.insert("", "end", values=(",".join(solution["colors"]), f"{solution['time']:.2f}"))


if __name__ == "__main__":
    app = WallPaintingApp()
    app.root.mainloop()
