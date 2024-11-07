import tkinter as tk
from tkinter import ttk, colorchooser

"""
FEATURES TO ADD:
1. Various configurations for each wall (color, pattern, etc.)
2. More refined look
3. Options to add multiple walls
"""

# Function to pick a color and update the preview
def pick_color(entry_var, color_button):
    """
    Opens a color chooser dialog to allow the user to select a color.
    Updates the color entry variable with the selected color and changes
    the background color of the button to show the chosen color visually.
    """
    color_code = colorchooser.askcolor(title="Choose Color")[1]
    if color_code:
        entry_var.set(color_code)  # Update the selected color variable
        color_button.config(bg=color_code)  # Update button to display color
        update_pattern()  # Refresh pattern preview after color change

# Function to update the pattern preview canvas
def update_pattern(event=None):
    """
    Clears and redraws the pattern preview based on the selected colors and pattern type.
    The pattern choice is determined by the selection in the combobox.
    This function is called whenever a color is chosen or pattern selection changes.
    """
    pattern_canvas.delete("all")  # Clear previous pattern
    colors = [selected_colors[i].get() for i in range(4)]  # Fetch selected colors

    # Draw each wall color on the canvas based on the selected pattern
    pattern = selector_combobox.get()
    if pattern == "Alternate":
        # Alternates between the first two selected colors
        for i in range(4):
            color = colors[i % 2]
            pattern_canvas.create_rectangle(i * 50, 0, (i + 1) * 50, 50, fill=color, outline="")
    elif pattern == "First and Last":
        # Colors the first and last wall with the first selected color, others with the second
        for i in range(4):
            color = colors[0] if i in {0, 3} else colors[1]
            pattern_canvas.create_rectangle(i * 50, 0, (i + 1) * 50, 50, fill=color, outline="")

# Set up the main window
root = tk.Tk()
root.title("Wall Painting Configuration")
root.geometry("400x450")
root.configure(bg="#F0F0F0")  # Light grey background for a modern look

# Style for ttk widgets
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), background="#F0F0F0")
style.configure("TButton", font=("Arial", 10), background="#FFFFFF", padding=6)

# Padding values
PADX, PADY = 5, 5

# Title label
label_title = ttk.Label(root, text="Wall-E Input", font=("Helvetica", 16))
label_title.grid(row=0, column=0, columnspan=3, pady=PADY+10)

# Room dimension inputs
dimensions = [("Wall Length (m):", 1), ("Wall Width (m):", 2), ("Wall Height (m):", 3)]
entries = []
for label_text, row in dimensions:
    label = ttk.Label(root, text=label_text)
    label.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
    entry = ttk.Entry(root)
    entry.grid(row=row, column=1, padx=PADX, pady=PADY)
    entries.append(entry)

# Wall color selection
selected_colors = [tk.StringVar(value="#ffffff") for _ in range(4)]
color_buttons = []

for i in range(2):
    # Helper function to ensure each color button has a unique reference
    def create_color_button(i):
        color_button = tk.Button(root, width=6, height=1, relief="solid", bg=selected_colors[i].get())
        # Configure button to open color picker and update its own color on click
        color_button.config(command=lambda var=selected_colors[i], btn=color_button: pick_color(var, btn))
        color_button.grid(row=4+i, column=1, padx=PADX, pady=PADY)
        color_buttons.append(color_button)
        return color_button

    # Initialize each color button
    color_button = create_color_button(i)

    # Label for each wall color
    label_color = ttk.Label(root, text=f"Wall {i+1} Color:")
    label_color.grid(row=4+i, column=0, padx=PADX, pady=PADY, sticky=tk.W)

# Pattern selection combobox and label
label_preview = ttk.Label(root, text="Select Pattern:")
label_preview.grid(row=9, column=0, padx=PADX, pady=PADY, sticky=tk.W)

# Combobox for selecting pattern; triggers update_pattern() on selection
selector_combobox = ttk.Combobox(root, values=["Alternate", "First and Last", "First and Second"], state="readonly")
selector_combobox.grid(row=9, column=1, padx=PADX, pady=PADY)
selector_combobox.bind("<<ComboboxSelected>>", update_pattern)

# Canvas for displaying a preview of the selected pattern and colors
pattern_canvas = tk.Canvas(root, width=200, height=50, bg="#FFFFFF", relief="solid")
pattern_canvas.grid(row=10, column=0, columnspan=3, padx=PADX, pady=PADY)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=lambda: print("Form Submitted"))
submit_button.grid(row=11, column=0, columnspan=3, pady=20)

# Initialize pattern preview with default selection
update_pattern()

# Run the GUI event loop
root.mainloop()
