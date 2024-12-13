import json
import heapq
from itertools import product
import numpy as np
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

class AStarPathfinder:
    def __init__(self, grid, doors):
        """Initialize with a grid and door positions."""
        self.grid = grid
        self.doors = doors

    def neighbors(self, node):
        """Find all walkable neighbors of the current node."""
        x, y, z = node
        neighbors = [
            (x + dx, y + dy, z + dz)
            for dx, dy, dz in [
                (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0),
                (0, 0, -1), (0, 0, 1)
            ]
            if 0 <= x + dx < len(self.grid) and 0 <= y + dy < len(self.grid[0])
            and 0 <= z + dz < len(self.grid[0][0])
            and self.grid[x + dx][y + dy][z + dz] == 0
        ]

        # Include door positions as valid neighbors
        for wall_id, door_info in self.doors.items():
            if tuple(door_info["position"]) == node:
                neighbors.append(tuple(door_info["position"]))

        return neighbors

    def find_path(self, start, goals):
        """Find the optimal path from start to one of the goal positions."""
        open_set = [(0, start)]  # Priority queue with (cost, node)
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goals[0])}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current in goals:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.neighbors(current):
                tentative_g_score = g_score[current] + 1  # Assume uniform cost for simplicity
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goals[0])
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No path found

    def heuristic(self, node, goal):
        """Simple Euclidean distance heuristic."""
        return np.linalg.norm(np.array(node) - np.array(goal))

    def reconstruct_path(self, came_from, current):
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]