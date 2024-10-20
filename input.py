import tkinter as tk
from tkinter import messagebox, colorchooser

def pick_color():
    # Opens the color picker dialog and returns the chosen color
    color_code = colorchooser.askcolor(title="Choose Room Color")
    if color_code:
        selected_color.set(color_code[1])  # Set the hex color code in the entry field

def submit_info():
    # Getting the user input
    length = entry_length.get()
    width = entry_width.get()
    height = entry_height.get()
    walls = entry_walls.get()
    color = selected_color.get()  # Get the color from the color picker
    pattern = entry_pattern.get()

    # Displaying the collected data
    room_config = f"Room Dimensions:\nLength: {length} m\nWidth: {width} m\nHeight: {height} m\nNumber of Walls: {walls}"
    paint_structure = f"\n\nPaint Structure:\nColor: {color}\nPattern: {pattern}"
    
    messagebox.showinfo("Room Configuration", room_config + paint_structure)

# Setting up the main window
root = tk.Tk()
root.title("Room Configuration")

# Room dimensions labels and entries
label_length = tk.Label(root, text="Room Length (in meters):")
label_length.pack()
entry_length = tk.Entry(root)
entry_length.pack()

label_width = tk.Label(root, text="Room Width (in meters):")
label_width.pack()
entry_width = tk.Entry(root)
entry_width.pack()

label_height = tk.Label(root, text="Room Height (in meters):")
label_height.pack()
entry_height = tk.Entry(root)
entry_height.pack()

label_walls = tk.Label(root, text="Number of Walls:")
label_walls.pack()
entry_walls = tk.Entry(root)
entry_walls.pack()

# Paint structure labels and entries
label_color = tk.Label(root, text="Paint Color:")
label_color.pack()

# Entry field to display the selected color
selected_color = tk.StringVar()
entry_color = tk.Entry(root, textvariable=selected_color)
entry_color.pack()

# Button to open color picker
color_button = tk.Button(root, text="Pick a Color", command=pick_color)
color_button.pack()

label_pattern = tk.Label(root, text="Paint Pattern:")
label_pattern.pack()
entry_pattern = tk.Entry(root)
entry_pattern.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_info)
submit_button.pack()

# Start the GUI event loop
root.mainloop()
