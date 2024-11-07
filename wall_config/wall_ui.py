import tkinter as tk
from tkinter import ttk, messagebox, colorchooser


"""
FEATURES TO ADD:
1. Various configurations for each wall (color, pattern, etc.)
2. More refined look
3. Options to add multiple walls
"""


def pick_color(entry_var):
    # Opens the color picker dialog and updates the selected color variable
    color_code = colorchooser.askcolor(title="Choose Color")[1]
    if color_code:
        entry_var.set(color_code)
        update_pattern()

def update_pattern():
    # Update the pattern display canvas with the selected colors for each wall
    pattern_canvas.delete("all")  # Clear the previous pattern
    colors = [selected_colors[i].get() for i in range(4)]
    
    # Draw each wall color on the canvas (for demonstration)
    for i, color in enumerate(colors):
        pattern_canvas.create_rectangle(i * 75, 0, (i + 1) * 75, 100, fill=color, outline="")

def submit_info():
    # Getting the user input
    length = entry_length.get()
    width = entry_width.get()
    height = entry_height.get()
    colors = [selected_colors[i].get() for i in range(4)]
    patterns = [pattern_vars[i].get() for i in range(4)]
    
    # Displaying the collected data for each wall
    room_config = f"Wall Dimensions:\nLength: {length} m\nWidth: {width} m\nHeight: {height} m\n"
    paint_structure = "\n\nPaint Structure:\n" + "\n".join([f"Wall {i+1} - Color: {colors[i]}, Pattern: {patterns[i]}" for i in range(4)])
    
    print("Room Configuration", room_config + paint_structure)

# Setting up the main window
root = tk.Tk()
root.title("Room Configuration")
root.geometry("500x700")  # Set window size
root.configure(bg="#F0F0F0")  # Light grey background for a modern look

# Style for modern UI using ttk
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), background="#F0F0F0")
style.configure("TButton", font=("Arial", 10), background="#FFFFFF", padding=6)
style.configure("TEntry", padding=6)

# Padding to improve layout
PADX, PADY = 10, 8

# Room dimensions labels and entries
label_title = ttk.Label(root, text="Wall-E input", font=("Helvetica", 18))
label_title.grid(row=0, column=0, columnspan=3, padx=180, pady=PADY+30, sticky=tk.W)


label_length = ttk.Label(root, text="Wall Length (in meters):")
label_length.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_length = ttk.Entry(root)
entry_length.grid(row=1, column=1, padx=PADX, pady=PADY)

label_width = ttk.Label(root, text="Wall Width (in meters):")
label_width.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_width = ttk.Entry(root)
entry_width.grid(row=2, column=1, padx=PADX, pady=PADY)

label_height = ttk.Label(root, text="Wall Height (in meters):")
label_height.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_height = ttk.Entry(root)
entry_height.grid(row=3, column=1, padx=PADX, pady=PADY)

# Wall configurations
selected_colors = []
pattern_vars = []
for i in range(4):
    selected_colors.append(tk.StringVar())
    pattern_vars.append(tk.StringVar(value="Pattern 1"))

    # Wall color selection
    label_color = ttk.Label(root, text=f"Wall {i+1} Color:")
    label_color.grid(row=4+i*2, column=0, padx=PADX, pady=PADY, sticky=tk.W)

    entry_color = ttk.Entry(root, textvariable=selected_colors[i], state='readonly')
    entry_color.grid(row=4+i*2, column=1, padx=PADX, pady=PADY)

    color_button = ttk.Button(root, text=f"Pick Color for Wall {i+1}", command=lambda var=selected_colors[i]: pick_color(var))
    color_button.grid(row=4+i*2, column=2, padx=PADX, pady=PADY)

# Display for visual pattern preview using Canvas
label_preview = ttk.Label(root, text="Pattern Preview:")
label_preview.grid(row=12, column=0, padx=PADX, pady=PADY, sticky=tk.W)

pattern_canvas = tk.Canvas(root, width=300, height=100, bg="#FFFFFF", relief="solid")
pattern_canvas.grid(row=13, column=0, columnspan=3, padx=PADX, pady=PADY)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit_info)
submit_button.grid(row=14, column=0, columnspan=3, pady=20)

# Start the GUI event loop
root.mainloop()