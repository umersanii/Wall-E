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

    def visualize_3d_environment(self, surfaces, path, original_path, colors):
        """Visualizes the 3D environment using matplotlib."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot each wall
        for surface, color in zip(surfaces, colors):

            x, y, z = surface["position"]

            if surface["orientation"] == "vertical":
                # Vertical walls: Span z-axis (height) and x-axis (width), fixed y
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y, y]  # Fixed y-coordinate for vertical walls
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
                
            elif surface["orientation"] == "vertical-x":
                # Vertical walls: Span z-axis (height) and x-axis (width), fixed y
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y, y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "vertical-y":
                # Vertical walls: Span z-axis (height) and y-axis (width), fixed x
                x_corners = [x, x, x, x]
                y_corners = [y, y + surface["width"], y + surface["width"], y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            vertices = [list(zip(x_corners, y_corners, z_corners))]
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, edgecolor=color, facecolors=color))

        # Plot the robot's traversal path
        if path:
            path_x, path_y, path_z = zip(*path)
            ax.plot(path_x, path_y, path_z, color='red', marker='o', label='Traversal Path')

            
            print(original_path)
            print(colors)
            # if path_x == original_path[0] and path_y == original_path[1] and path_z == original_path[2]:
            #     ax.plot(path_x, path_y, path_z, color=colors[], marker='o', label='Original Path')

        # Set labels and limits
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([0, max(surface["position"][0] + surface["width"] for surface in surfaces) + 1])
        ax.set_ylim([0, max(surface["position"][1] + surface["height"] for surface in surfaces) + 1])
        ax.set_zlim([0, max(surface["position"][2] + surface["height"] for surface in surfaces) + 1])

        plt.title("3D Wall Painting Environment")
        plt.legend()
        plt.show()



    def solve_csp(self):
        """Greedy approach to solve CSP with constraints."""
        surface_positions = [surface["position"] for surface in self.surfaces]
        optimal_path = self.a_star_pathfinding(self.start_position, surface_positions)

        total_time = 0
        paint_usage = {color: 0 for color in self.colors}
        color_assignment = []
        path_index = 0

        for surface in self.surfaces:
            assigned_color = None
            for color in self.colors:
                # Check paint availability
                if paint_usage[color] + surface["area"] > self.paint_availability.get(color, float('inf')):
                    continue

                # Check adjacency constraints
                if self.adjacency_constraint and path_index > 0:
                    if color == color_assignment[-1]:  # Adjacent walls cannot have the same color
                        continue

                # Assign the color if all constraints are met
                assigned_color = color
                paint_usage[color] += surface["area"]
                color_assignment.append(color)
                break

            # If no color could be assigned, terminate (invalid solution)
            if not assigned_color:
                print(f"Failed to assign color for wall {surface['id']}.")
                return []

            # Calculate painting time
            painting_time = surface["area"] * self.time_per_meter
            total_time += painting_time

            # Calculate travel time
            if path_index > 0:
                travel_distance = np.linalg.norm(
                    np.array(optimal_path[path_index]) - np.array(optimal_path[path_index - 1])
                )
                travel_time = travel_distance / 2.0
                total_time += travel_time

            path_index += 1

        # Validate the solution
        if total_time > self.max_time:
            print("Total time exceeds the maximum allowed time.")
            return []

        return [{
            "colors": color_assignment,
            "total_time": total_time,
            "path": optimal_path,
            "paint_usage": paint_usage
        }]

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
        self.visualize_3d_environment(self.surfaces, solutions[0]["path"], solutions[0]["path"], solutions[0]["colors"])


# Main execution
if __name__ == "__main__":
    complex_input_data = {
   "surfaces": [
        # Room 1 Walls (forming a closed room)
        {"id": 1, "height": 3.0, "width": 4.0, "position": [0, 0, 0], "orientation": "vertical-x"},  
        {"id": 2, "height": 3.0, "width": 4.0, "position": [4, 0, 0], "orientation": "vertical-y"},  
        {"id": 3, "height": 3.0, "width": 4.0, "position": [0, 4, 0], "orientation": "vertical-x"}, 
        {"id": 4, "height": 3.0, "width": 4.0, "position": [0, 0, 0], "orientation": "vertical-y"}, 

        # Room 2 Walls
        {"id": 5, "height": 3.0, "width": 4.0, "position": [8, 0, 0], "orientation": "vertical-x"},  
        {"id": 6, "height": 3.0, "width": 4.0, "position": [12, 0, 0], "orientation": "vertical-y"}, 
        {"id": 7, "height": 3.0, "width": 4.0, "position": [8, 4, 0], "orientation": "vertical-x"}, 
        {"id": 8, "height": 3.0, "width": 4.0, "position": [8, 0, 0], "orientation": "vertical-y"},

        # Room 1 to Room 2 Door
        {"id": 9, "height": 2.0, "width": 1.0, "position": [4, 2, 0], "orientation": "vertical"},  

        # Room 3 Walls
        {"id": 10, "height": 3.0, "width": 4.0, "position": [0, 8, 0], "orientation": "vertical-x"}, 
        {"id": 11, "height": 3.0, "width": 4.0, "position": [4, 8, 0], "orientation": "vertical-y"}, 
        {"id": 12, "height": 3.0, "width": 4.0, "position": [0, 12, 0], "orientation": "vertical-x"}, 
        {"id": 13, "height": 3.0, "width": 4.0, "position": [0, 8, 0], "orientation": "vertical-y"},  

        # Room 2 to Room 3 Door
        {"id": 14, "height": 2.0, "width": 1.0, "position": [8, 4, 0], "orientation": "horizontal"}  
    ],
    "colors": ["White", "Yellow", "Blue"],
    "time_per_meter": 2.0,
    "max_time": 30000.0,
    "paint_availability": {
        "White": 15,
        "Yellow": 2000,
        "Blue": 1500,
        "Black": 1005,
        "Red": 1000
    },
    "adjacency_constraint": True,
    "min_colors": 5,
    "start_position": [0, 0, 0] }
    input_data = {
   "surfaces": [
        # Room 1 Walls (forming a closed room)
        {"id": 1, "height": 3.0, "width": 4.0, "position": [0, 0, 0], "orientation": "vertical-x"}, 
        {"id": 2, "height": 3.0, "width": 4.0, "position": [4, 0, 0], "orientation": "vertical-y"},  

    ],
    "colors": ["White", "Yellow", "Blue"],
    "time_per_meter": 2.0,
    "max_time": 30000.0,
    "paint_availability": {
        "White": 15,
        "Yellow": 2000,
        "Blue": 1500,
        "Black": 1005,
        "Red": 1000
    },
    "adjacency_constraint": True,
    "min_colors": 5,
    "start_position": [0, 0, 0] }
 
    solver = WallPaintingSolver3D(complex_input_data)
    solutions = solver.solve_csp()
    solver.display_solutions(solutions)
