# Wall-E
`Wall-E` is a Python-based tool that solves a **constraint satisfaction problem (CSP)** for optimizing the painting of walls in a 3D environment. It assigns colors to walls based on user-defined constraints like paint availability, adjacency rules, and time limits, while visualizing the walls and robot traversal in 3D.

---

### **Features**
- **Constraint-Based Painting Optimization:**
  - Assigns colors to walls while adhering to adjacency rules and paint availability.
  - Computes the shortest traversal path using A* pathfinding.
  - Minimizes painting and travel time.
- **3D Visualization:**
  - Renders walls with their assigned colors and plots the robot’s traversal path.
- **Dynamic Input Support:**
  - User-configurable wall definitions, constraints, and robot properties.

---

### **Setup**

#### **Requirements**
- Python 3.8+
- Required Libraries:
  - `numpy`
  - `matplotlib`
  - `pyqt5`

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### **Usage**

#### **1. Define Input**
Create a JSON input file (e.g., `input.json`) with the following structure:
```json
{
   "surfaces": [
        {"id": 1, "height": 3.0, "width": 4.0, "position": [0, 0, 0], "orientation": "vertical-x"},
        {"id": 2, "height": 3.0, "width": 4.0, "position": [4, 0, 0], "orientation": "vertical-y"}
   ],
   "colors": ["White", "Yellow", "Blue"],
   "time_per_meter": 2.0,
   "max_time": 300.0,
   "paint_availability": {"White": 15, "Yellow": 10, "Blue": 10},
   "adjacency_constraint": true,
   "min_colors": 2,
   "start_position": [0, 0, 0]
}
```

#### **2. Run the Solver**
Run the script with your input file:
```bash
python main.py
```

#### **3. Output**
The solver provides:
- Assigned colors for walls.
- Total painting and travel time.
- Paint usage.
- 3D visualization of the environment.

---

### **Example Output**
```plaintext
=== Valid Solutions ===

Solution 1:
  - Total Time: 60.00 minutes
  - Colors Used: White, Yellow
  - Paint Usage: {'White': 12.0, 'Yellow': 12.0, 'Blue': 0.0}
  - Optimal Path: [(0, 0, 0), (4, 0, 0)]
----------------------------------------
```

---

### **Planned Features**
- **Interactive 3D Visualization:** Inspect and modify wall configurations dynamically.
- **Multiple Rooms Support:** Seamlessly handle complex environments with multiple connected rooms.
- **Export Options:** Save results and visualizations as images or 3D models.

---

### **Contributing**
Contributions are welcome! Please:
1. Fork the repository.
2. Submit a pull request with a detailed explanation of your changes.

---

