import json
import heapq
from itertools import product
import numpy as np

class WallPaintingSolver:
    def __init__(self, input_data):
        self.input_data = input_data
        self.surfaces = self.parse_surfaces(input_data["surfaces"])
        self.colors = input_data["colors"]
        self.time_per_meter = input_data["time_per_meter"]
        self.max_time = input_data["max_time"]
        self.start_position = tuple(input_data["start_position"])

    @staticmethod
    def parse_surfaces(surfaces):
        """Parses surface data and calculates area."""
        parsed_surfaces = []
        for surface in surfaces:
            height = surface["height"]
            width = surface["width"]
            parsed_surfaces.append({
                "id": surface["id"],
                "height": height,
                "width": width,
                "area": height * width,
                "position": tuple(surface["position"])
            })
        return parsed_surfaces

    def a_star_pathfinding(self, start, goals):
        """Finds the shortest path to cover all goals using A*."""
        def heuristic(a, b):
            return np.linalg.norm(np.array(a) - np.array(b))  # Euclidean distance

        path = [start]
        remaining_goals = goals[:]
        while remaining_goals:
            current = path[-1]
            distances = [(heuristic(current, goal), goal) for goal in remaining_goals]
            distances.sort()
            _, next_goal = distances[0]
            path.append(next_goal)
            remaining_goals.remove(next_goal)
        return path

    def solve_csp(self):
        """Solves the painting CSP problem with additional constraints."""
        # Extract surface positions
        surface_positions = [surface["position"] for surface in self.surfaces]

        # Calculate optimal path order using A*
        optimal_path = self.a_star_pathfinding(self.start_position, surface_positions)

        # Generate all possible color combinations
        color_combinations = list(product(self.colors, repeat=len(self.surfaces)))

        # Paint availability (in square meters)
        paint_availability = {
            "White": 15,
            "Yellow": 1,
            "Blue": 11,
            "Black": 12,
            "Red": 5
        }

        valid_solutions = []
        for combination in color_combinations:
            total_time = 0
            paint_usage = {color: 0 for color in self.colors}
            path_index = 0
            is_valid = True

            for surface, color in zip(self.surfaces, combination):
                # Painting time
                painting_time = surface["area"] * self.time_per_meter
                total_time += painting_time

                # Update paint usage
                paint_usage[color] += surface["area"]
                if paint_usage[color] > paint_availability[color]:
                    is_valid = False
                    break

                # Travel time
                if path_index > 0:
                    travel_distance = np.linalg.norm(
                        np.array(optimal_path[path_index]) - np.array(optimal_path[path_index - 1])
                    )
                    travel_time = travel_distance / 2.0  # Assuming speed = 2 units/sec
                    total_time += travel_time

                # Adjacency constraints
                if path_index > 0 and combination[path_index] == combination[path_index - 1]:
                    is_valid = False
                    break

                path_index += 1

            if is_valid and total_time <= self.max_time:
                valid_solutions.append({
                    "colors": combination,
                    "total_time": total_time,
                    "path": optimal_path
                })

        # Sort solutions by time and return the top solutions
        valid_solutions.sort(key=lambda x: x["total_time"])
        return valid_solutions[:10]

    def to_json(self, solutions):
        """Converts the solutions to JSON format."""
        return json.dumps(solutions, indent=4)

    def display_solutions(self, solutions):
        """Displays the valid solutions in a structured, readable format."""
        if not solutions:
            print("No valid solutions found.")
            return

        print("=== Valid Solutions ===\n")
        for idx, solution in enumerate(solutions, start=1):
            print(f"Solution {idx}:")
            print(f"  - Total Time: {solution['total_time']:.2f} minutes")
            print(f"  - Colors Used: {', '.join(solution['colors'])}")
            print(f"  - Optimal Path: {solution['path']}")
            print("-" * 40)

# Main execution
if __name__ == "__main__":
    # Example input
    input_data = {
        "surfaces": [
            {"id": 1, "height": 2.5, "width": 3.0, "position": [1, 1]},
            {"id": 2, "height": 2.0, "width": 2.5, "position": [4, 4]},
            {"id": 3, "height": 3.0, "width": 2.0, "position": [6, 2]},
            {"id": 4, "height": 2.5, "width": 2.5, "position": [8, 5]},
            {"id": 5, "height": 2.0, "width": 3.0, "position": [3, 7]}
        ],
        "colors": ["White", "Black", "Yellow", "Red", "Blue"],
        "time_per_meter": 2.0,
        "max_time": 100.0,
        "start_position": [0, 0]
    }

    # Initialize solver
    solver = WallPaintingSolver(input_data)

    # Solve the problem
    solutions = solver.solve_csp()

    # Output solutions as JSON
    print("=== Valid Solutions ===")
    solver.display_solutions(solutions)
   