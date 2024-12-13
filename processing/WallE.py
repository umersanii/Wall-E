import json
import heapq
from itertools import product
import numpy as np
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from algorithims.astar import AStarPathfinder
from algorithims.csp import CSPColorAssigner

class WallE:
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
        self.doors = {surface["id"]: surface for surface in self.surfaces if "door" in surface}

        # Instantiate sub-modules
        self.grid = self.create_grid(input_data["surfaces"])
        self.pathfinder = AStarPathfinder(self.grid, self.doors)


        # Instantiate sub-modules
        self.pathfinder = AStarPathfinder(grid=self.grid, doors=self.doors)
        self.csp_solver = CSPColorAssigner(
            self.colors, self.paint_availability, self.adjacency_constraint, self.min_colors
        )

    @staticmethod
    def parse_surfaces(surfaces):
        """Parses surface data and calculates area."""
        parsed_surfaces = []
        for surface in surfaces:
            height = surface["height"]
            width = surface["width"]
            position = tuple(surface["position"])
            orientation = surface.get("orientation", "Vertical")
            parsed_surfaces.append({
                "id": surface["id"],
                "height": height,
                "width": width,
                "area": height * width,
                "position": position,
                "orientation": orientation
            })
        return parsed_surfaces

    def create_grid(self, surfaces):
        """Create a grid representation of the environment."""
        max_x = max(s["position"][0] + s["width"] for s in surfaces)
        max_y = max(s["position"][1] + s["height"] for s in surfaces)
        max_z = max(s["position"][2] + s["height"] for s in surfaces)
        grid = np.zeros((int(max_x), int(max_y), int(max_z)))

        for surface in surfaces:
            x, y, z = surface["position"]
            grid[x:x + surface["width"], y:y + surface["height"], z:z + surface["height"]] = 1  # Mark as occupied

        return grid
    
    def solve(self):
        """Solve the wall painting problem."""
        # Find the optimal path using A* pathfinding
        surface_positions = [surface["position"] for surface in self.surfaces]
        optimal_path = self.pathfinder.find_path(self.start_position, surface_positions)

        # Assign colors using the CSP solver
        color_assignment, paint_usage = self.csp_solver.color_assign(self.surfaces)
        if not color_assignment:
            print("No valid solutions: Constraints could not be satisfied.")
            return None

        # Calculate total time
        total_time = 0
        for idx, surface in enumerate(self.surfaces):
            painting_time = surface["area"] * self.time_per_meter
            total_time += painting_time

            if idx > 0:
                travel_distance = np.linalg.norm(
                    np.array(optimal_path[idx]) - np.array(optimal_path[idx - 1])
                )
                travel_time = travel_distance / 2.0
                total_time += travel_time

        if total_time > self.max_time:
            print("No valid solutions: Exceeds maximum allowed time.")
            return None

        print("Total time: ", total_time)
        print("Paint usage: ", paint_usage)
        print("Path: ", optimal_path)
        print("Color assignment: ", color_assignment)

        # Return the solution
        return {
            "colors": color_assignment,
            "total_time": total_time,
            "path": optimal_path,
            "paint_usage": paint_usage
        }

    def visualize_3d_environment(self, surfaces, path, colors):
        """Visualizes the 3D environment using matplotlib."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Plot each wall with its assigned color
        for surface, color in zip(surfaces, colors):
            x, y, z = surface["position"]

            if surface["orientation"] == "Vertical-x":
                # Vertical wall spans z (height) and x (width)
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y, y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "Vertical-y":
                # Vertical wall spans z (height) and y (width)
                x_corners = [x, x, x, x]
                y_corners = [y, y + surface["width"], y + surface["width"], y]
                z_corners = [z, z, z + surface["height"], z + surface["height"]]
            elif surface["orientation"] == "horizontal":
                # Horizontal wall spans x (width) and y (height)
                x_corners = [x, x + surface["width"], x + surface["width"], x]
                y_corners = [y, y, y + surface["height"], y + surface["height"]]
                z_corners = [z, z, z, z]

            vertices = [list(zip(x_corners, y_corners, z_corners))]
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, edgecolor=color, facecolors=color))

        # Plot traversal path
        if path:
            path_x, path_y, path_z = zip(*path)
            ax.plot(path_x, path_y, path_z, color="red", marker="o", label="Traversal Path")

        # Set labels and limits
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim([0, max(surface["position"][0] + surface["width"] for surface in surfaces) + 1])
        ax.set_ylim([0, max(surface["position"][1] + surface["height"] for surface in surfaces) + 1])
        ax.set_zlim([0, max(surface["position"][2] + surface["height"] for surface in surfaces) + 1])

        plt.title("3D Wall Painting Environment")
        plt.legend()
        plt.show()

    def display_solutions(self, solution):
        """Displays the solution and visualizes the 3D environment."""
        if not solution:
            print("No valid solutions found.")
            return

        print("=== Solution ===")
        print(f"  - Total Time: {solution['total_time']:.2f} minutes")
        print(f"  - Colors Used: {', '.join(solution['colors'])}")
        print(f"  - Paint Usage: {solution['paint_usage']}")
        print(f"  - Optimal Path: {solution['path']}")

        # Visualize the solution
        self.visualize_3d_environment(self.surfaces, solution["path"], solution["colors"])

