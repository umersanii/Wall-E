import tkinter as tk
from tkinter import ttk, colorchooser

"""
FEATURES TO ADD:
1. Various configurations for each wall (color, pattern, etc.)
2. More refined look
3. Options to add multiple walls
"""

class WallUI:
    def __init__(self, root=None):
        """Initializes the wall UI components."""
        if root is None:
            self.root = tk.Tk()  # Create a new Tkinter window if none is passed
        else:
            self.root = root 
        self.root.title("Wall Painting Configuration")
        self.root.geometry("400x450")
        self.root.configure(bg="#F0F0F0")  # Light grey background for a modern look

        # Padding values
        self.PADX, self.PADY = 5, 5

        # Initialize the required variables for room dimensions, wall colors, etc.
        self.entries = []
        self.selected_colors = [tk.StringVar(value="#ffffff") for _ in range(4)]

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        """Sets up all the widgets for the UI."""
        # Style for ttk widgets
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10), background="#F0F0F0")
        style.configure("TButton", font=("Arial", 10), background="#FFFFFF", padding=6)

        # Title label
        label_title = ttk.Label(self.root, text="Wall-E Input", font=("Helvetica", 16))
        label_title.grid(row=0, column=0, columnspan=3, pady=self.PADY+10)

        # Room dimension inputs
        dimensions = [("Wall Length (m):", 1), ("Wall Width (m):", 2), ("Wall Height (m):", 3)]
        for label_text, row in dimensions:
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=row, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.W)
            entry = ttk.Entry(self.root)
            entry.grid(row=row, column=1, padx=self.PADX, pady=self.PADY)
            self.entries.append(entry)

        # Wall color selection
        color_buttons = []
        for i in range(2):
            # Helper function to ensure each color button has a unique reference
            def create_color_button(i):
                color_button = tk.Button(self.root, width=6, height=1, relief="solid", bg=self.selected_colors[i].get())
                # Configure button to open color picker and update its own color on click
                color_button.config(command=lambda var=self.selected_colors[i], btn=color_button: self.pick_color(var, btn))
                color_button.grid(row=4+i, column=1, padx=self.PADX, pady=self.PADY)
                color_buttons.append(color_button)
                return color_button

            # Initialize each color button
            color_button = create_color_button(i)

            # Label for each wall color
            label_color = ttk.Label(self.root, text=f"Wall {i+1} Color:")
            label_color.grid(row=4+i, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.W)

        # Pattern selection combobox and label
        label_preview = ttk.Label(self.root, text="Select Pattern:")
        label_preview.grid(row=9, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.W)

        # Combobox for selecting pattern; triggers update_pattern() on selection
        self.selector_combobox = ttk.Combobox(self.root, values=["Alternate", "First and Last", "First and Second"], state="readonly")
        self.selector_combobox.grid(row=9, column=1, padx=self.PADX, pady=self.PADY)
        self.selector_combobox.bind("<<ComboboxSelected>>", self.update_pattern)

        # Canvas for displaying a preview of the selected pattern and colors
        self.pattern_canvas = tk.Canvas(self.root, width=200, height=50, bg="#FFFFFF", relief="solid")
        self.pattern_canvas.grid(row=10, column=0, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Submit button
        submit_button = ttk.Button(self.root, text="Submit")
        submit_button.grid(row=11, column=0, columnspan=3, pady=20)
        submit_button.config(command=self.submit_form)

        # Initialize pattern preview with default selection
        self.update_pattern()

    def pick_color(self, entry_var, color_button):
        """
        Opens a color chooser dialog to allow the user to select a color.
        Updates the color entry variable with the selected color and changes
        the background color of the button to show the chosen color visually.
        """
        color_code = colorchooser.askcolor(title="Choose Color")[1]
        if color_code:
            entry_var.set(color_code)  # Update the selected color variable
            color_button.config(bg=color_code)  # Update button to display color
            self.update_pattern()  # Refresh pattern preview after color change

    def update_pattern(self, event=None):
        """
        Clears and redraws the pattern preview based on the selected colors and pattern type.
        The pattern choice is determined by the selection in the combobox.
        This function is called whenever a color is chosen or pattern selection changes.
        """
        self.pattern_canvas.delete("all")  # Clear previous pattern
        colors = [self.selected_colors[i].get() for i in range(4)]  # Fetch selected colors

        # Draw each wall color on the canvas based on the selected pattern
        pattern = self.selector_combobox.get()
        if pattern == "Alternate":
            # Alternates between the first two selected colors
            for i in range(4):
                color = colors[i % 2]
                self.pattern_canvas.create_rectangle(i * 50, 0, (i + 1) * 50, 50, fill=color, outline="")
        elif pattern == "First and Last":
            # Colors the first and last wall with the first selected color, others with the second
            for i in range(4):
                color = colors[0] if i in {0, 3} else colors[1]
                self.pattern_canvas.create_rectangle(i * 50, 0, (i + 1) * 50, 50, fill=color, outline="")

    def submit_form(self):
        """
        Extracts room dimensions, wall colors, and the selected pattern from the UI elements.
        This function is called when the form is submitted.

        - Room dimensions are extracted from the entries.
        - Wall colors are extracted from the selected color variables.
        - The selected pattern is extracted from the combobox.

        The collected information is then printed or processed as needed.
        """
        # Extract room dimensions
        length = self.entries[0].get()
        width = self.entries[1].get()
        height = self.entries[2].get()

        # Extract wall colors
        colors = [color_var.get() for color_var in self.selected_colors]

        # Extract selected pattern
        selected_pattern = self.selector_combobox.get()

        # # Print or process the collected information
        # print("Room Dimensions - Length:", length, "Width:", width, "Height:", height)
        # print("Wall Colors:", colors)
        # print("Selected Pattern:", selected_pattern)
        return (length, width, height, colors, selected_pattern)
    def get_wall_config(self):
        """
        Returns the wall configuration data as a dictionary after the user submits the form.
        """
        # Assuming the form was submitted successfully and wall configuration is needed
        length = self.entries[0].get()
        width = self.entries[1].get()
        height = self.entries[2].get()
        colors = [color_var.get() for color_var in self.selected_colors]
        pattern = self.selector_combobox.get()

        return {
            "length": length,
            "width": width,
            "height": height,
            "colors": colors,
            "pattern": pattern
        }

    def show(self):
        """
        Starts the Tkinter mainloop to display the UI window.
        """
        self.root.mainloop()

