from ui import UI
# from floor_navigation.floor_ui import FloorUI
# from floor_navigation.navigation_ui import NavigationUI
 from algorithms.a_star import a_star
# from algorithms.csp import CSP
# import wall_processing
# import floor_processing

def main():
    # Initialize the UnifiedUI component (which includes WallUI, FloorUI, etc.)
    unified_ui = UI()

    # Show the unified UI interface
    unified_ui.show()

    # At this point, the UI is running and handling its own event loop.
    # When the user interacts with the UI, the processing will be triggered.

    # You may want to use methods from unified_ui to access configurations
    # when the UI triggers data processing (this happens in the background).

    # Example: Get Wall configuration after UI interaction
    # wall_config = unified_ui.wall_ui.get_wall_config()  # Example of retrieving wall config

    # Processing is done within the UI's event loop asynchronously, as needed.
    # Example of processing after gathering wall configuration:
    # wall_processed = wall_processing.process_wall_data(wall_config)
    # print("Processed Wall Data:", wall_processed)

    # Similarly, Floor or Navigation configurations can be processed if needed.

if __name__ == "__main__":
    main()
