## **Documentation: WALL E**

### **Overview**
The `WALL E` class solves a **constraint satisfaction problem (CSP)** for painting walls in a 3D environment. The algorithm optimizes wall painting under constraints like paint availability, adjacency rules, and time limits, while visualizing the walls and traversal paths in 3D.

---

### **Key Functionalities**

#### **1. Input Structure**
The input is a JSON object with the following fields:
- **`surfaces`**: List of wall definitions with attributes:
  - `id`: Unique wall identifier.
  - `height`, `width`: Dimensions of the wall.
  - `position`: Starting point `[x, y, z]` in 3D space.
  - `orientation`: Orientation of the wall:
    - `"vertical-x"`: Vertical wall spanning the **x-axis** and **z-axis**.
    - `"vertical-y"`: Vertical wall spanning the **y-axis** and **z-axis**.
    - `"horizontal"`: Horizontal wall spanning the **x-axis** and **y-axis**.
- **`colors`**: List of available colors for painting.
- **`time_per_meter`**: Time required to paint 1 square meter.
- **`max_time`**: Maximum allowed painting time.
- **`paint_availability`**: Paint quantities available per color.
- **`adjacency_constraint`**: Boolean to enforce different colors for adjacent walls.
- **`min_colors`**: Minimum number of distinct colors to use.
- **`start_position`**: Starting position of the robot in 3D space.

---

#### **2. Core Methods**

##### **`parse_surfaces`**
Parses and processes wall data from the input:
- Computes the area of each wall (`height * width`).
- Prepares data for pathfinding and visualization.

##### **`a_star_pathfinding`**
Implements the **A*** algorithm to calculate the shortest path through all walls:
- Uses 3D Euclidean distance as the heuristic.
- Returns the ordered list of positions for traversal.

##### **`solve_csp`**
Solves the CSP using a **greedy algorithm**:
- Assigns colors to walls, respecting:
  - **Paint availability**: Ensures sufficient paint for each wall.
  - **Adjacency rules**: Prevents adjacent walls from having the same color.
  - **Time constraints**: Ensures total painting and travel time are within limits.
- Returns valid solutions, including:
  - Assigned colors for walls.
  - Total time required.
  - Paint usage.
  - Robot's traversal path.

##### **`visualize_3d_environment`**
Renders the walls and robot’s traversal path in a 3D environment using `matplotlib`:
- Colors each wall according to its assigned color.
- Plots the robot's traversal path as a red line.
- Provides a clear view of the environment with labeled axes.

##### **`display_solutions`**
Displays solutions in a readable format:
- Prints the assigned colors, total time, paint usage, and path for each solution.
- Invokes the `visualize_3d_environment` function for the best solution.

---

### **How to Use**

#### **1. Input Example**
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

#### **2. Instantiate and Run Solver**
```python
solver = WallPaintingSolver3D(input_data)
solutions = solver.solve_csp()
solver.display_solutions(solutions)
```

---

### **Output**
The solver outputs valid solutions with:
1. **Colors Used**: Assigned colors for each wall.
2. **Total Time**: Combined painting and travel time.
3. **Paint Usage**: Quantity of each paint used.
4. **Path**: Robot's traversal path through the walls.

Example:
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

### **Error Handling**
- **No Valid Solutions**: If constraints cannot be satisfied, prints:
  ```plaintext
  No valid solutions found.
  ```
- **Constraint Violations**: Debug messages explain violations like:
  - Paint limits exceeded.
  - Time exceeds `max_time`.

---

### **Visualization**
The 3D visualization shows:
- **Walls**: Rendered in their assigned colors.
- **Traversal Path**: A red line connecting the walls in the optimal sequence.

---

### **Code Structure**
- **Class Definition:** `WallPaintingSolver3D`.
- **Key Functions:** `parse_surfaces`, `solve_csp`, `visualize_3d_environment`.
- **Main Script:** Instantiates the solver, solves the problem, and displays results.

*Written by ChatGPT*