## **Documentation: WALL-E**

### **Overview**
The `WALL-E` application is a wall-painting solver for a **constraint satisfaction problem (CSP)**. It optimizes wall painting in a 3D environment under constraints like paint availability, adjacency rules, and time limits. The application includes a **graphical user interface (GUI)** for interactive input and visualization of results.

---

### **Key Functionalities**

#### **1. GUI Features**
The application includes a PyQt5-based GUI for user-friendly interaction. Key screens include:

##### **Welcome Screen**
- **Buttons**:
  - **Manual Input**: Switches to a screen for entering inputs manually.
  - **Load JSON File**: Allows users to load inputs from a JSON file.
  - **Test Sample JSON**: Loads a predefined JSON sample for testing purposes.

##### **Manual Input Screen**
Allows users to specify details about walls, constraints, and other parameters interactively:
- **Dynamic Wall Inputs**: Users can specify the number of walls and dynamically provide details for each wall (height, width, position, orientation).
- **Additional Parameters**:
  - Available colors (comma-separated).
  - Time required to paint one square meter.
  - Maximum allowed painting time.
  - Minimum number of distinct colors.
  - Starting position of the robot.
- **Submit Button**: Validates inputs, constructs the JSON data, and solves the CSP.

##### **Error Handling in GUI**
- Input validation for all fields.
- Pop-up messages for errors (e.g., missing fields, invalid formats).

---

#### **2. Input Structure**
The input is either entered manually in the GUI or loaded from a JSON file. The structure includes:
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
- **`paint_availability`** (optional in manual input): Paint quantities per color.
- **`adjacency_constraint`**: Boolean to enforce different colors for adjacent walls.
- **`min_colors`**: Minimum number of distinct colors to use.
- **`start_position`**: Starting position of the robot in 3D space.

---

#### **3. Core Methods**

##### **Solver Class: `WallE`**

###### **`parse_surfaces`**
Parses and processes wall data from the input:
- Computes the area of each wall (`height * width`).
- Prepares data for pathfinding and visualization.

###### **`a_star_pathfinding`**
Implements the **A*** algorithm to calculate the shortest path through all walls:
- Uses 3D Euclidean distance as the heuristic.
- Returns the ordered list of positions for traversal.

###### **`solve_csp`**
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

###### **`visualize_3d_environment`**
Renders the walls and robot’s traversal path in a 3D environment using `matplotlib`:
- Colors each wall according to its assigned color.
- Plots the robot's traversal path as a red line.
- Provides a clear view of the environment with labeled axes.

###### **`display_solutions`**
Displays solutions in a readable format:
- Prints the assigned colors, total time, paint usage, and path for each solution.
- Invokes the `visualize_3d_environment` function for the best solution.

---

### **How to Use**

#### **1. GUI Workflow**
1. **Launch the Application**:
   Run the script to start the GUI.
2. **Choose an Input Method**:
   - **Manual Input**: Enter data interactively.
   - **Load JSON File**: Load input from a file.
   - **Test Sample JSON**: Use a predefined sample for testing.
3. **Submit**:
   - After entering the data, click **Submit**.
   - The solution is calculated, and the result is displayed in the console and via visualization.

#### **2. Input Example for JSON File**
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

---

### **Output**

#### **Console Output**
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

#### **Visualization**
The 3D visualization shows:
- **Walls**: Rendered in their assigned colors.
- **Traversal Path**: A red line connecting the walls in the optimal sequence.

---

### **Error Handling**
- **Invalid Inputs**:
  - The GUI validates all inputs and displays error messages for invalid entries.
  - Examples: Non-numeric values, missing fields.
- **No Valid Solutions**:
  If constraints cannot be satisfied, prints:
  ```plaintext
  No valid solutions found.
  ```


*Written by ChatGPT*