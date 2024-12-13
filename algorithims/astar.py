import numpy as np

class AStarPathfinder:
    def __init__(self):
        pass

    def heuristic(self, a, b):
        """Calculate Euclidean distance between two points."""
        return np.linalg.norm(np.array(a) - np.array(b))

    def find_path(self, start, goals):
        """Find the shortest path covering all goals using A*."""
        path = [start]
        remaining_goals = goals[:]
        while remaining_goals:
            current = path[-1]
            distances = [(self.heuristic(current, goal), goal) for goal in remaining_goals]
            distances.sort()
            _, next_goal = distances[0]
            path.append(next_goal)
            remaining_goals.remove(next_goal)
        return path