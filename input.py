import tkinter as tk
from tkinter import ttk, messagebox, colorchooser

def pick_color1():
    # Opens the color picker dialog and updates the first color
    color_code = colorchooser.askcolor(title="Choose First Color")[1]
    if color_code:
        selected_color1.set(color_code)
        update_pattern()

def pick_color2():
    # Opens the color picker dialog and updates the second color
    color_code = colorchooser.askcolor(title="Choose Second Color")[1]
    if color_code:
        selected_color2.set(color_code)
        update_pattern()

def update_pattern():
    # Update the pattern display canvas with the selected colors
    color1 = selected_color1.get()
    color2 = selected_color2.get()
    pattern_canvas.delete("all")  # Clear the previous pattern
    pattern_canvas.create_rectangle(0, 0, 150, 100, fill=color1, outline="")
    pattern_canvas.create_rectangle(150, 0, 300, 100, fill=color2, outline="")

def submit_info():
    # Getting the user input
    length = entry_length.get()
    width = entry_width.get()
    height = entry_height.get()
    walls = entry_walls.get()
    color1 = selected_color1.get()  # First color
    color2 = selected_color2.get()  # Second color
    pattern = pattern_var.get()     # Get selected pattern

    # Displaying the collected data
    room_config = f"Room Dimensions:\nLength: {length} m\nWidth: {width} m\nHeight: {height} m\nNumber of Walls: {walls}"
    paint_structure = f"\n\nPaint Structure:\nFirst Color: {color1}\nSecond Color: {color2}\nPattern: {pattern}"
    
    messagebox.showinfo("Room Configuration", room_config + paint_structure)

# Setting up the main window
root = tk.Tk()
root.title("Room Configuration")
root.geometry("500x600")  # Set window size
root.configure(bg="#F0F0F0")  # Light grey background for a modern look

# Style for modern UI using ttk
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), background="#F0F0F0")
style.configure("TButton", font=("Arial", 10), background="#FFFFFF", padding=6)
style.configure("TEntry", padding=6)

# Padding to improve layout
PADX, PADY = 10, 8

# Room dimensions labels and entries
label_length = ttk.Label(root, text="Room Length (in meters):")
label_length.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_length = ttk.Entry(root)
entry_length.grid(row=0, column=1, padx=PADX, pady=PADY)

label_width = ttk.Label(root, text="Room Width (in meters):")
label_width.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_width = ttk.Entry(root)
entry_width.grid(row=1, column=1, padx=PADX, pady=PADY)

label_height = ttk.Label(root, text="Room Height (in meters):")
label_height.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_height = ttk.Entry(root)
entry_height.grid(row=2, column=1, padx=PADX, pady=PADY)

label_walls = ttk.Label(root, text="Number of Walls:")
label_walls.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=tk.W)
entry_walls = ttk.Entry(root)
entry_walls.grid(row=3, column=1, padx=PADX, pady=PADY)

# Paint structure labels and entries
label_color1 = ttk.Label(root, text="First Wall Color:")
label_color1.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=tk.W)

# Entry field to display the first selected color
selected_color1 = tk.StringVar()
entry_color1 = ttk.Entry(root, textvariable=selected_color1, state='readonly')
entry_color1.grid(row=4, column=1, padx=PADX, pady=PADY)

# Button to open color picker for the first color
color_button1 = ttk.Button(root, text="Pick First Color", command=pick_color1)
color_button1.grid(row=4, column=2, padx=PADX, pady=PADY)

label_color2 = ttk.Label(root, text="Second Wall Color:")
label_color2.grid(row=5, column=0, padx=PADX, pady=PADY, sticky=tk.W)

# Entry field to display the second selected color
selected_color2 = tk.StringVar()
entry_color2 = ttk.Entry(root, textvariable=selected_color2, state='readonly')
entry_color2.grid(row=5, column=1, padx=PADX, pady=PADY)

# Button to open color picker for the second color
color_button2 = ttk.Button(root, text="Pick Second Color", command=pick_color2)
color_button2.grid(row=5, column=2, padx=PADX, pady=PADY)

# Paint Pattern Selection
label_pattern = ttk.Label(root, text="Select Paint Pattern:")
label_pattern.grid(row=6, column=0, padx=PADX, pady=PADY, sticky=tk.W)

# Radio buttons for predefined patterns
pattern_var = tk.StringVar(value="Pattern 1")
radio_pattern1 = ttk.Radiobutton(root, text="Pattern 1 (Two-tone)", variable=pattern_var, value="Pattern 1", command=update_pattern)
radio_pattern1.grid(row=6, column=1, padx=PADX, pady=PADY, sticky=tk.W)

radio_pattern2 = ttk.Radiobutton(root, text="Pattern 2 (Solid Color)", variable=pattern_var, value="Pattern 2", command=update_pattern)
radio_pattern2.grid(row=7, column=1, padx=PADX, pady=PADY, sticky=tk.W)

# Display for visual pattern preview using Canvas
label_preview = ttk.Label(root, text="Pattern Preview:")
label_preview.grid(row=8, column=0, padx=PADX, pady=PADY, sticky=tk.W)

pattern_canvas = tk.Canvas(root, width=300, height=100, bg="#FFFFFF", relief="solid")
pattern_canvas.grid(row=9, column=0, columnspan=3, padx=PADX, pady=PADY)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit_info)
submit_button.grid(row=10, column=0, columnspan=3, pady=20)

# Start the GUI event loop
root.mainloop()
