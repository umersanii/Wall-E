import heapq
import time


# Constants
WALL = '-'
OBSTACLE = 'O'
EMPTY = ' '
AGENT = 'A'
GOAL = 'G'
gridSize=0

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


#heuristic function
def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

#function to check for valid moves
def is_valid(grid, x, y, energy):
    size = len(grid)
    if 0 <= x < size and 0 <= y < size:  # Check bounds
        if grid[x][y] != WALL and energy > 0:  # Check if it's not a wall and energy is available
            return True
    return False


#function to get valid neighbors 
def get_neighbors(grid, x, y, energy):
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if is_valid(grid, nx, ny, energy):
            energy_cost = 2 if grid[nx][ny] == OBSTACLE else 1
            neighbors.append((nx, ny, energy_cost))
    return neighbors


#Actual A* Star Algo
def a_star(grid, start_x, start_y, goal_x, goal_y, max_energy):
    queue = []
    heapq.heappush(queue, (0, (start_x, start_y), [(start_x, start_y)]))
    visited = set()
    energy = max_energy
    total_cost = 0
    nodes_explored = 0

    start_time = time.time()  # Start time measurement

    while queue:
        current_cost, (x, y), path = heapq.heappop(queue)

        if (x, y) in visited:
            continue
        visited.add((x, y))
        total_cost = current_cost  # Update total cost
        nodes_explored += 1  # Count nodes explored

        if (x, y) == (goal_x, goal_y):
            elapsed_time = time.time() - start_time  # End time measurement
            return path, total_cost, elapsed_time, nodes_explored

        for nx, ny, energy_cost in get_neighbors(grid, x, y, energy):
            if (nx, ny) not in visited:
                new_cost = current_cost + energy_cost
                heuristic_cost = heuristic(nx, ny, goal_x, goal_y)
                estimated_total_cost = new_cost + heuristic_cost
                new_path = path + [(nx, ny)]
                heapq.heappush(queue, (estimated_total_cost, (nx, ny), new_path))

    elapsed_time = time.time() - start_time  # End time measurement
    return None, total_cost, elapsed_time, nodes_explored  # No path found
