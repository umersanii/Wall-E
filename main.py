# main.py
from wall_config.wall_ui import WallUI
from floor_navigation.floor_ui import FloorUI
from floor_navigation.navigation_ui import NavigationUI
from algorithms.a_star import AStar
from algorithms.csp import CSP

def main():
    # Initialize UI components
    wall_ui = WallUI()
    floor_ui = FloorUI()
    nav_ui = NavigationUI()

    # Show and manage the application interface
    wall_ui.show()
    floor_ui.show()
    nav_ui.show()

    # Example of how to use processing functions or algorithms
    # after gathering all required inputs
    wall_config = wall_ui.get_wall_config()
    floor_config = floor_ui.get_floor_config()
    nav_config = nav_ui.get_navigation_config()

    # Process wall and floor data
    wall_processed = wall_processing.process_wall_data(wall_config)
    floor_processed = floor_processing.process_floor_data(floor_config)

    # Run A* algorithm if necessary
    path = AStar().find_path(nav_config, floor_processed)

    # Display results, handle further processing

if __name__ == "__main__":
    main()
