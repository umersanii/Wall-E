class CSPColorAssigner:
    def __init__(self, colors, paint_availability, adjacency_constraint, min_colors):
        self.colors = colors
        self.paint_availability = paint_availability
        self.adjacency_constraint = adjacency_constraint
        self.min_colors = min_colors

    def color_assign(self, surfaces):
        """Assign colors to walls while satisfying constraints."""
        paint_usage = {color: 0 for color in self.colors}
        color_assignment = []

        for idx, surface in enumerate(surfaces):
            assigned_color = None
            for color in self.colors:
                # Check paint availability
                if paint_usage[color] + surface["area"] > self.paint_availability.get(color, float('inf')):
                    continue

                # Check adjacency constraints
                if self.adjacency_constraint and idx > 0:
                    if color == color_assignment[-1]:  # Adjacent walls cannot have the same color
                        continue

                # Assign the color if all constraints are met
                assigned_color = color
                paint_usage[color] += surface["area"]
                color_assignment.append(color)
                break

            # If no valid color was found, return failure
            if not assigned_color:
                print(f"Failed to assign color for wall {surface['id']}. Insufficient colors or paint.")
                return None, None

        # Ensure minimum color diversity
        if len(set(color_assignment)) < self.min_colors:
            print(f"Failed to satisfy minimum color diversity: {len(set(color_assignment))} < {self.min_colors}.")
            return None, None

        return color_assignment, paint_usage
