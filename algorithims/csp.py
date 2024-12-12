class CSPColorAssigner:
    def __init__(self, colors, paint_availability, adjacency_constraint, min_colors):
        self.colors = colors
        self.paint_availability = paint_availability
        self.adjacency_constraint = adjacency_constraint
        self.min_colors = min_colors

    def color_assign(self, surfaces):
        """Assign colors to walls while satisfying adjacency and minimum color constraints."""
        paint_usage = {color: 0 for color in self.colors}
        color_assignment = {}
        used_colors = set()  # Track the set of colors used

        # Dynamically compute adjacency list
        adjacency_list = self._calculate_adjacency_list(surfaces)
        print("Adjacency List:", adjacency_list)  # Debugging: Verify adjacency list

        def backtrack(index):
            if index == len(surfaces):
                # Ensure at least the required number of colors are used
                if len(used_colors) < self.min_colors:
                    return False
                return True

            surface = surfaces[index]
            surface_id = surface["id"]
            surface_area = surface["height"] * surface["width"]

            for color in self.colors:
                # Skip the color if it exceeds the required number of colors used
                if len(used_colors) >= self.min_colors and color not in used_colors:
                    continue

                # Check paint availability
                if paint_usage[color] + surface_area > self.paint_availability.get(color, float('inf')):
                    continue

                # Check adjacency constraints
                if all(color_assignment.get(neighbor) != color for neighbor in adjacency_list[surface_id]):
                    # Assign the color
                    color_assignment[surface_id] = color
                    paint_usage[color] += surface_area
                    used_colors.add(color)  # Track that this color is being used

                    if backtrack(index + 1):
                        return True

                    # Backtrack
                    paint_usage[color] -= surface_area
                    del color_assignment[surface_id]
                    if paint_usage[color] == 0:
                        used_colors.remove(color)  # Remove color from used colors when backtracking

            return False

        if backtrack(0):
            return color_assignment, paint_usage
        else:
            print("Failed to find a valid color assignment.")
            return None, None

    def _calculate_adjacency_list(self, surfaces):
        """Dynamically calculate adjacency list based on surface corners."""
        adjacency_list = {surface["id"]: [] for surface in surfaces}
        for i, surface1 in enumerate(surfaces):
            for j, surface2 in enumerate(surfaces):
                if i != j and self._are_adjacent(surface1, surface2):
                    adjacency_list[surface1["id"]].append(surface2["id"])
        return adjacency_list

    def _are_adjacent(self, surface1, surface2):
        """Determine if two surfaces are adjacent based on their corner coordinates."""
        corners1 = self.compute_surface_corners(surface1)
        corners2 = self.compute_surface_corners(surface2)

        # Check if any of the corners overlap or share a boundary
        for corner1 in corners1:
            for corner2 in corners2:
                if corner1 == corner2:
                    return True  # Overlapping corner

        # Check for shared edges (for surfaces that don't overlap completely)
        # Compare x or y coordinates of the corners for shared boundaries
        for i in range(4):
            for j in range(4):
                if self._is_edge_shared(corners1[i], corners1[(i+1)%4], corners2[j], corners2[(j+1)%4]):
                    return True  # Shared edge
        return False

    def _is_edge_shared(self, corner1, corner2, corner3, corner4):
        """Check if two edges (formed by corner pairs) share a boundary."""
        return (
            (corner1[0] == corner2[0] == corner3[0] == corner4[0] and  # Same x-coordinate (vertical alignment)
             min(corner1[1], corner2[1]) <= corner3[1] <= max(corner1[1], corner2[1]) and
             min(corner1[1], corner2[1]) <= corner4[1] <= max(corner1[1], corner2[1])) or
            (corner1[1] == corner2[1] == corner3[1] == corner4[1] and  # Same y-coordinate (horizontal alignment)
             min(corner1[0], corner2[0]) <= corner3[0] <= max(corner1[0], corner2[0]) and
             min(corner1[0], corner2[0]) <= corner4[0] <= max(corner1[0], corner2[0]))
        )

    def compute_surface_corners(self, surface):
        """Compute the four corners of a surface based on position, height, and width."""
        x, y, z = surface["position"]
        height = surface["height"]
        width = surface["width"]
        
        if surface["orientation"] == "Vertical-x":
            return [
                (x, y, z),
                (x + width, y, z),
                (x + width, y + height, z),
                (x, y + height, z)
            ]
        elif surface["orientation"] == "Vertical-y":
            return [
                (x, y, z),
                (x, y + width, z),
                (x, y + width, z + height),
                (x, y, z + height)
            ]
        elif surface["orientation"] == "horizontal":
            return [
                (x, y, z),
                (x + width, y, z),
                (x + width, y + height, z),
                (x, y + height, z)
            ]
        return []

# Sample input
sample_data = {
    "surfaces": [
        {"id": 1, "height": 3, "width": 6, "position": [0, 0, 0], "orientation": "Vertical-x"},
        {"id": 2, "height": 3, "width": 6, "position": [0, 6, 0], "orientation": "Vertical-x"},
        {"id": 3, "height": 3, "width": 6, "position": [6, 0, 0], "orientation": "Vertical-y"},
        {"id": 4, "height": 3, "width": 6, "position": [0, 0, 0], "orientation": "Vertical-y"}
    ],
    "colors": ["Red", "Yellow", "Blue", "White", "Black"],
    "time_per_meter": 2.0,
    "max_time": 30000.0,
    "paint_availability": {
        "White": 150,
        "Yellow": 2000,
        "Blue": 150,
        "Black": 1005,
        "Red": 1000
    },
    "adjacency_constraint": True,
    "min_colors": 2,
    "start_position": [0, 0, 0]
}

# Create the CSPColorAssigner instance
assigner = CSPColorAssigner(
    colors=sample_data["colors"],
    paint_availability=sample_data["paint_availability"],
    adjacency_constraint=sample_data["adjacency_constraint"],
    min_colors=sample_data["min_colors"]
)

# Compute adjacency list and color assignment
adjacency_list = assigner._calculate_adjacency_list(sample_data["surfaces"])
print("Adjacency List:", adjacency_list)

# Try to assign colors
color_assignment, paint_usage = assigner.color_assign(sample_data["surfaces"])
print("Color Assignment:", color_assignment)
print("Paint Usage:", paint_usage)
