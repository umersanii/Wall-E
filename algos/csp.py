from itertools import permutations

class WallPaintingCSP:
    def __init__(self, walls, colors, constraints):
        """
        Initialize the WallPaintingCSP instance.

        Args:
            walls (list): List of walls (e.g., ["Wall 1", "Wall 2", ...]).
            colors (list): List of available colors (e.g., ["#FF0000", "#00FF00", "#0000FF"]).
            constraints (list of tuples): List of adjacency constraints (e.g., [("Wall 1", "Wall 2"), ...]).
        """
        self.walls = walls
        self.colors = colors
        self.constraints = constraints
        self.assignment = {}

    def is_assignment_valid(self, wall, color):
        """
        Check if assigning a color to a wall is valid with current constraints.

        Args:
            wall (str): The wall to which color is assigned.
            color (str): The color to assign to the wall.

        Returns:
            bool: True if assignment is valid; False otherwise.
        """
        for (w1, w2) in self.constraints:
            # Check if wall has constraints with another wall
            if wall == w1 and w2 in self.assignment:
                if self.assignment[w2] == color:
                    return False
            elif wall == w2 and w1 in self.assignment:
                if self.assignment[w1] == color:
                    return False
        return True

    def backtrack(self):
        """
        Backtracking algorithm to find a valid color assignment for each wall.

        Returns:
            dict: A valid color assignment for each wall if possible; otherwise, None.
        """
        # If all walls are assigned, return assignment
        if len(self.assignment) == len(self.walls):
            return self.assignment

        # Select the next wall to assign
        wall = self.select_unassigned_wall()

        # Try assigning each color to the selected wall
        for color in self.colors:
            if self.is_assignment_valid(wall, color):
                # Assign color to wall
                self.assignment[wall] = color

                # Recursively attempt to assign colors to remaining walls
                result = self.backtrack()
                if result:
                    return result

                # If assignment fails, backtrack
                del self.assignment[wall]

        return None

    def select_unassigned_wall(self):
        """
        Select an unassigned wall.

        Returns:
            str: The next unassigned wall.
        """
        for wall in self.walls:
            if wall not in self.assignment:
                return wall

    def solve(self):
        """
        Solve the CSP problem for wall painting.

        Returns:
            dict: A valid color assignment if possible; otherwise, None.
        """
        return self.backtrack()

"""
Might need to be changed after adding more walls
"""
# Define constants for walls
WALL_1 = "Wall 1"
WALL_2 = "Wall 2"
WALL_3 = "Wall 3"
WALL_4 = "Wall 4"

# Define the walls, available colors, and adjacency constraints
walls = [WALL_1, WALL_2, WALL_3, WALL_4]
colors = ["#FF0000", "#00FF00", "#0000FF"]  # Add more colors as needed
constraints = [(WALL_1, WALL_2), (WALL_2, WALL_3), (WALL_3, WALL_4), (WALL_4, WALL_1)]

# Initialize and solve the CSP
wall_painting_csp = WallPaintingCSP(walls, colors, constraints)
solution = wall_painting_csp.solve()

if solution:
    print("A valid color assignment for walls is:")
    for wall, color in solution.items():
        print(f"{wall}: {color}")
else:
    print("No valid assignment found.")
