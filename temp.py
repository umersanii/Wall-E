import json
import heapq
from itertools import product
import numpy as np
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

class WallPaintingSolver3D:
    def __init__(self, input_data):
        self.input_data = input_data
        self.surfaces = self.parse_surfaces(input_data["surfaces"])
        self.colors = input_data["colors"]
        self.time_per_meter = input_data["time_per_meter"]
        self.max_time = input_data["max_time"]
        self.paint_availability = input_data.get("paint_availability", {})
        self.adjacency_constraint = input_data.get("adjacency_constraint", True)
        self.min_colors = input_data.get("min_colors", 3)
        self.start_position = tuple(input_data["start_position"])

    @staticmethod
    def parse_surfaces(surfaces):
        """Parses surface data and calculates area."""
        parsed_surfaces = []
        for surface in surfaces:
            height = surface["height"]
            width = surface["width"]
            position = tuple(surface["position"])
            orientation = surface.get("orientation", "vertical")
            parsed_surfaces.append({
                "id": surface["id"],
                "height": height,
                "width": width,
                "area": height * width,
                "position": position,
                "orientation": orientation
            })
        return parsed_surfaces

    def a_star_pathfinding(self, start, goals):
        """Finds the shortest path to cover all goals using A* in 3D."""
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

    def visualize_3d_environment(self, surfaces, path):
        """Visualizes the 3D environment using matplotlib."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot each wall
        for surface in surfaces:
            x, y, z = surface["position"]
            if surface["orientation"] == "vertical":
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y, y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "horizontal":
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y + surface["height"], y + surface["height"], y]
                z_corners = [z, z, z, z]

            vertices = [list(zip(x_corners, y_corners, z_corners))]
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, edgecolor='k'))

        # Plot the robot's traversal path
        path_x, path_y, path_z = zip(*path)
        ax.plot(path_x, path_y, path_z, color='red', marker='o', label='Traversal Path')

        # Set labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.legend()
        plt.show()

    def solve_csp(self):
        """Modified solve_csp for 3D environment with added randomness and penalties."""
        surface_positions = [surface["position"] for surface in self.surfaces]
        optimal_path = self.a_star_pathfinding(self.start_position, surface_positions)

        color_combinations = list(product(self.colors, repeat=len(self.surfaces)))
        valid_solutions = []
        for combination in color_combinations:
            total_time = 0
            paint_usage = {color: 0 for color in self.colors}
            path_index = 0
            is_valid = True
            distinct_colors = set()

            for surface, color in zip(self.surfaces, combination):
                painting_time = surface["area"] * self.time_per_meter
                total_time += painting_time

                paint_usage[color] += surface["area"]
                if self.paint_availability and paint_usage[color] > self.paint_availability.get(color, float('inf')):
                    is_valid = False
                    break

                if self.adjacency_constraint and path_index > 0:
                    if combination[path_index] == combination[path_index - 1]:
                        is_valid = False
                        break

                distinct_colors.add(color)

                if path_index > 0:
                    travel_distance = np.linalg.norm(
                        np.array(optimal_path[path_index]) - np.array(optimal_path[path_index - 1])
                    )
                    travel_time = travel_distance / 2.0
                    total_time += travel_time

                path_index += 1

            if len(distinct_colors) < self.min_colors:
                is_valid = False

            if is_valid and total_time <= self.max_time:
                valid_solutions.append({
                    "colors": combination,
                    "total_time": total_time,
                    "path": optimal_path,
                    "paint_usage": paint_usage
                })

        valid_solutions = sorted(valid_solutions, key=lambda x: x["total_time"])
        return valid_solutions[:10]

    def display_solutions(self, solutions):
        """Displays solutions and visualizes the 3D environment."""
        if not solutions:
            print("No valid solutions found.")
            return

        print("=== Valid Solutions ===\n")
        for idx, solution in enumerate(solutions, start=1):
            print(f"Solution {idx}:")
            print(f"  - Total Time: {solution['total_time']:.2f} minutes")
            print(f"  - Colors Used: {', '.join(solution['colors'])}")
            print(f"  - Paint Usage: {solution['paint_usage']}")
            print(f"  - Optimal Path: {solution['path']}")
            print("-" * 40)

        # Visualize the 3D environment for the best solution
        self.visualize_3d_environment(self.surfaces, solutions[0]["path"])


# Main execution
if __name__ == "__main__":
    input_data = {
        "surfaces": [
            {"id": 1, "height": 3.0, "width": 4.0, "position": [0, 2, 0], "orientation": "vertical"},
            {"id": 2, "height": 2.5, "width": 3.5, "position": [5, 2, 0], "orientation": "vertical"},
            {"id": 3, "height": 4.0, "width": 3.0, "position": [7, 3, 3], "orientation": "vertical"},
            {"id": 2, "height": 2.5, "width": 3.5, "position": [8, 2, 0], "orientation": "vertical"},

        ],
        "colors": ["White", "Yellow", "Blue", "Black", "Red"],
        "time_per_meter": 2.5,
        "max_time": 1050.0,
        "paint_availability": {
            "White": 20,
            "Yellow": 15,
            "Blue": 12,
            "Black": 10,
            "Red": 8
        },
        "adjacency_constraint": False,
        "min_colors": 2,
        "start_position": [0, 0, 0]
    }

    solver = WallPaintingSolver3D(input_data)
    solutions = solver.solve_csp()
    solver.display_solutions(solutions)
