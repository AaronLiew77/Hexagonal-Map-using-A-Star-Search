import math
import tkinter as tk
from tkinter import font

# Constants for GUI display
HEX_SIZE = 35
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
COLOR_ORANGE = "#ffb74d"  # Orange
COLOR_TURQOISE = "#4db6ac"  # Turqoise
COLOR_VIOLET = "#ce93d8"
COLOR_PURPLE = "#7986cb"
ANIMATION_DELAY = 600  # Delay between each step of the animation in milliseconds

# Create GUI function used to call the GUI in the main file


def create_gui(hex_map, path, max_weight, max_size):
    # Filter out string keys from hex_map
    hex_coordinates = [node for node in hex_map if isinstance(
        node, tuple) and len(node) == 2]

    # Calculate the total grid width and height
    grid_width = HEX_SIZE * 1.5 * \
        (max(node[0] for node in hex_coordinates) + 2)
    grid_height = HEX_SIZE * \
        math.sqrt(3) * (max(node[1] for node in hex_coordinates) + 1.5)

    # Calculate the center offset for the grid
    offset_x = (CANVAS_WIDTH - grid_width) / 2 - 150
    offset_y = (CANVAS_HEIGHT - grid_height) / 2 - 50

    # Initialize the window for the GUI and its title
    window = tk.Tk()
    window.title("Ronny Rubbish Maze Problem")

    # Set the fixed size of the window
    window.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    window.resizable(0, 0)  # Disable window resizing

    # Canvas to display the hexagonal grid
    canvas = tk.Canvas(window, width=CANVAS_WIDTH,
                       height=CANVAS_HEIGHT, bg="#40444b")
    canvas.pack(side=tk.LEFT)

    # Drawing the hexagonal grid here
    for node in hex_map:
        if isinstance(node, tuple) and len(node) == 2 and node != 'rubbish_bin':
            x, y = node
        else:
            continue

        # Coordinate system to make the top start with (0,5)
        y = 5 - y

        # Calculate the center position of the hexagon
        center_x = x * HEX_SIZE * 1.5 + HEX_SIZE + offset_x

        if x % 2 == 1:
            center_y = y * HEX_SIZE * \
                math.sqrt(3) + HEX_SIZE * math.sqrt(3) / 2 + offset_y
        else:
            center_y = y * HEX_SIZE * \
                math.sqrt(3) + HEX_SIZE * math.sqrt(3) + offset_y

        points = [
            center_x - HEX_SIZE, center_y,
            center_x - HEX_SIZE / 2, center_y + HEX_SIZE * 0.85,
            center_x + HEX_SIZE / 2, center_y + HEX_SIZE * 0.85,
            center_x + HEX_SIZE, center_y,
            center_x + HEX_SIZE / 2, center_y - HEX_SIZE * 0.85,
            center_x - HEX_SIZE / 2, center_y - HEX_SIZE * 0.85
        ]

        # Colored hexagons representing the weight and size of the rubbish room according to the assignment
        if node in [(2, 2), (3, 2), (7, 4), (8, 1)]:
            canvas.create_polygon(points, outline="black", fill=COLOR_ORANGE)
        elif node in [(0, 2), (3, 5), (5, 4), (8, 3), (9,3)]:
            canvas.create_polygon(points, outline="black", fill=COLOR_TURQOISE)
        elif node in [(1, 4), (7, 1)]:
            canvas.create_polygon(points, outline="black", fill=COLOR_VIOLET)
        elif node in [(5, 2), (8, 5)]:
            canvas.create_polygon(points, outline="black", fill=COLOR_PURPLE)
        elif node in [(0, 5), (4, 0), (7, 5), (8, 2)]:
            canvas.create_polygon(points, outline="black", fill="yellow")
            canvas.create_text(center_x, center_y + 15, text="DISPOSAL", fill="black", font=("Arial", 5, "bold"))  

        else:
            canvas.create_polygon(points, outline="black", fill="white")

        display_y = 5 - y

        # Display the coordinates on the hexagon
        canvas.create_text(center_x, center_y,
                           text=f"({x}, {display_y})", fill="black")

    # Rectangular container below the grid
    container_width = grid_width
    container_height = 80
    container_x = offset_x
    container_y = offset_y + grid_height + 20
    container = canvas.create_rectangle(
        container_x, container_y, container_x + container_width, container_y + container_height, fill="white"
    )

    # Label for the current path
    path_label = canvas.create_text(
        container_x + container_width / 2, container_y + container_height / 6, text="", fill="black", font=font.Font(weight="bold"), anchor='n'
    )

    # Label for the action
    action_label = canvas.create_text(
        container_x + container_width / 2,
        container_y + container_height - 10,
        text="",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='s'
    )

    # Rectangular container beside the grid (right-top)
    container_width = 300
    container_height = 200
    container_x = offset_x + grid_width + 20
    container_y = offset_y + 20
    container = canvas.create_rectangle(
        container_x, container_y, container_x + container_width, container_y + container_height, fill="white"
    )

    # Label for the "Node Information" section
    info_label_title = canvas.create_text(
        container_x + 15,
        container_y + 5,
        text="Node Information:",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='nw'
    )

    # Label for the weight & volume
    info_label = canvas.create_text(
        container_x + container_width / 2,
        container_y + container_height / 2,
        text="",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='s'
    )

    # Label for the accumulated weight & volume
    total_label = canvas.create_text(
        container_x + container_width / 2,
        container_y + container_height - 20,
        text="",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='s'
    )

    # Rectangular container beside the grid (right-bottom)
    container_width = 300
    container_height = 200
    container_x = offset_x + grid_width + 20
    container_y = grid_height - offset_y - 20
    container = canvas.create_rectangle(
        container_x, container_y, container_x + container_width, container_y + container_height, fill="white"
    )

    # Label for the "Node Information" section
    bin_label_title = canvas.create_text(
        container_x + 15,
        container_y + 5,
        text="Rubbish Bin Information:",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='nw'
    )

    # Label for the weight & volume
    bin_label = canvas.create_text(
        container_x + container_width / 2,
        container_y + container_height / 2,
        text="",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='s'
    )

    # Label for the accumulated weight & volume
    bin_status_label = canvas.create_text(
        container_x + container_width / 2,
        container_y + container_height - 40,
        text="",
        fill="black",
        font=font.Font(weight="bold"),
        anchor='s'
    )

    # Initialize accumulated total weight and size variables
    total_info = {"current_total_weight": 0, "current_total_size": 0}

    # Initialize rubbish bin available weight and size variables
    available_info = {"available_weight": max_weight, "available_size": max_size}

    # Animation function to update the arrow positions and display node info
    def animate_arrows(step=1):
        if step < len(path):
            # Get the coordinates of the current and next step
            x1, y1 = path[step - 1]
            x2, y2 = path[step]

            # Modify the y-coordinates based on the coordinate system
            y1 = 5 - y1
            y2 = 5 - y2

            # Calculate the center position of the hexagons in the path
            center_x1 = x1 * HEX_SIZE * 1.5 + HEX_SIZE + offset_x
            center_x2 = x2 * HEX_SIZE * 1.5 + HEX_SIZE + offset_x

            if x1 % 2 == 1:
                center_y1 = y1 * HEX_SIZE * \
                    math.sqrt(3) + HEX_SIZE * math.sqrt(3) / 2 + offset_y
            else:
                center_y1 = y1 * HEX_SIZE * \
                    math.sqrt(3) + HEX_SIZE * math.sqrt(3) + offset_y

            if x2 % 2 == 1:
                center_y2 = y2 * HEX_SIZE * \
                    math.sqrt(3) + HEX_SIZE * math.sqrt(3) / 2 + offset_y
            else:
                center_y2 = y2 * HEX_SIZE * \
                    math.sqrt(3) + HEX_SIZE * math.sqrt(3) + offset_y

            # Calculate the angle and length of the arrow
            angle = math.atan2(center_y2 - center_y1, center_x2 - center_x1)
            arrow_length = HEX_SIZE * 0.5

            # Calculate the coordinates of the arrowhead
            arrow_x = center_x1 + (HEX_SIZE * 0.9) * math.cos(angle)
            arrow_y = center_y1 + (HEX_SIZE * 0.9) * math.sin(angle)

            # Draw the arrow line and arrowhead
            arrow_color = "#a1e2a1"
            canvas.create_line(center_x1, center_y1, center_x2,
                               center_y2, fill=arrow_color, width=2, arrow=tk.LAST)
            canvas.create_text((center_x1 + center_x2) / 2, (center_y1 + center_y2) / 2, text=str(step),
                               fill="black", font=font.Font(weight="bold"))
            canvas.create_line(center_x2, center_y2, arrow_x,
                               arrow_y, fill=arrow_color, width=2)
            canvas.create_line(
                center_x2,
                center_y2,
                arrow_x + arrow_length * math.cos(angle - math.pi / 6),
                arrow_y + arrow_length * math.sin(angle - math.pi / 6),
                fill=arrow_color,
                width=2,
            )
            canvas.create_line(
                center_x2,
                center_y2,
                arrow_x + arrow_length * math.cos(angle + math.pi / 6),
                arrow_y + arrow_length * math.sin(angle + math.pi / 6),
                fill=arrow_color,
                width=2,
            )

            # Update the canvas
            canvas.update()

            # Update the current path label
            current_path = f"Current Path: ({x2}, {5 - y2})"
            canvas.itemconfigure(path_label, text=current_path)

            # Call the display_node_info function to display weight and volume information
            display_node_info((x2, 5 - y2))

            # Schedule the next animation step
            window.after(ANIMATION_DELAY, lambda: animate_arrows(step + 1))

        else:
            # Animation finished, display the entire path
            path_text = "All rubbish cleared"
            canvas.itemconfigure(path_label, text=path_text)

            # Show total cost
            action_info = f"Total Cost: {len(path)}"
            canvas.itemconfigure(action_label, text=action_info)

    # Function to display weight and volume information for a node
    def display_node_info(node):
        # Clear previous weight and volume information
        canvas.itemconfigure(info_label, text="")

        # Check if the node is a rubbish node and has a non-zero weight and non-zero volume
        if hex_map[node]["rubbish"] and hex_map[node]["weight"] != 0 and hex_map[node]["volume"] != 0:
            weight = hex_map[node]["weight"]
            volume = hex_map[node]["volume"]

            # Update the current accumulated collected rubbish weight and size
            total_info["current_total_weight"] += weight
            total_info["current_total_size"] += volume

            # Update the current available rubbish weight and size
            available_info["available_weight"] -= weight
            available_info["available_size"] -= volume

            # Set collected node weight & volume to 0
            hex_map[node]["weight"] = 0
            hex_map[node]["volume"] = 0

            # Create a text string to display weight and volume
            weight_volume_info = f"Current Weight: {weight} kg\nCurrent Volume: {volume} m\u00B3"
            canvas.itemconfigure(info_label, text=weight_volume_info)

            # Calculate the center position of the hexagon
            x, y = node
            center_x = x * HEX_SIZE * 1.5 + HEX_SIZE + offset_x
            if x % 2 == 1:
                center_y = (5 - y) * HEX_SIZE * math.sqrt(3) + \
                    HEX_SIZE * math.sqrt(3) / 2 + offset_y
            else:
                center_y = (5 - y) * HEX_SIZE * math.sqrt(3) + \
                    HEX_SIZE * math.sqrt(3) + offset_y

            # Display "CLEARED" text inside the hexagon
            canvas.create_text(center_x, center_y + 15, text="CLEARED",
                               fill="black", font=("Arial", 5, "bold"))

            # Show action
            action_info = f"Found rubbish at {node}"
            canvas.itemconfigure(action_label, text=action_info)

            # Check if the available weight and size is 0 (not able to collect rubbish anymore)
            if available_info["available_weight"] == 0 or available_info["available_size"] == 0:
                # Display rubbish bin status
                status_info = "Status: Full"
                canvas.itemconfigure(bin_status_label, text=status_info)
            
            # The rubbish bin not full yet
            else:
                # Display rubbish bin status
                status_info = "Status: Available"
                canvas.itemconfigure(bin_status_label, text=status_info)

        # Check if the node is the disposal node
        elif node in [(0, 5), (4, 0), (7, 5), (8, 2)]:
            # Show action
            action_info = f"Disposed rubbish of total {total_info['current_total_weight']} kg and {total_info['current_total_size']} m\u00B3 at {node}"
            canvas.itemconfigure(action_label, text=action_info)

            # If the node is the disposal node, reset the accumulated weight and size to 0
            total_info["current_total_weight"] = 0
            total_info["current_total_size"] = 0

            # Update the current available rubbish weight and size to max weight and size
            available_info["available_weight"] = max_weight
            available_info["available_size"] = max_size

            # Create a text string to display node information
            weight_volume_info = "Disposal room"
            canvas.itemconfigure(info_label, text=weight_volume_info)

            # Display rubbish bin status
            status_info = "Status: Available"
            canvas.itemconfigure(bin_status_label, text=status_info)

        # Check if the node is an empty room
        else:
            # Create a text string to display node information
            weight_volume_info = "Empty room"
            canvas.itemconfigure(info_label, text=weight_volume_info)

            # Check if the current accumulated total weight and size is 40 kg or 5 m^3
            if total_info["current_total_weight"] == max_weight or total_info["current_total_size"] == max_size:
                # Show action
                action_info = f"Searching for nearest disposal room..."
                canvas.itemconfigure(action_label, text=action_info)

                # Display rubbish bin status
                status_info = "Status: Full"
                canvas.itemconfigure(bin_status_label, text=status_info)

            # The accumulated collected weight not 40kg or 5 m^3
            else:
                # Show action
                action_info = f"Searching for nearest rubbish room..."
                canvas.itemconfigure(action_label, text=action_info)

                # Display rubbish bin status
                status_info = "Status: Available"
                canvas.itemconfigure(bin_status_label, text=status_info)

        # Create a text string to display weight and volume
        accumulated_info = f"Accumulated Weight: {total_info['current_total_weight']} kg\nAccumulated Volume: {total_info['current_total_size']} m\u00B3"
        canvas.itemconfigure(total_label, text=accumulated_info)

        # Create a text string to display weight and volume
        bin_info = f"Available Weight: {available_info['available_weight']} kg\nAvailable Volume: {available_info['available_size']} m\u00B3"
        canvas.itemconfigure(bin_label, text=bin_info)

    # Start the animation
    animate_arrows()

    # Start the GUI event loop
    window.mainloop()