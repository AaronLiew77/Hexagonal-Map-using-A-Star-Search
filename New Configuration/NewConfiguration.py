import math
import heapq
from NewConfigurationGUI import create_gui
import time

# Start the timer
start_time = time.time()

# Calculate the Euclidean distance between two nodes
def euclidean_distance(node_a, node_b):
    du = node_a[0] - node_b[0]
    dv = node_a[1] - node_b[1]
    dx = math.sqrt(3) * du / 2
    dy = (1 - (-1) ** du) / 4 + dv
    return math.sqrt(dx ** 2 + dy ** 2)


# Maximum weight and size of rubbish bin
max_weight = 50
max_size = 10

# Define the map, initialize the rubbish bin and start node position
hex_map = {
    'rubbish_bin': {
        'capacity': max_weight,
        'volume': max_size,
        'start': (0, 0)
    },
}

# Define the disposal rooms position
disposal_rooms = [(0, 5), (4, 0), (7, 5), (8, 2)]
# row and column of the size of hexagon map
col = 10
row = 6

# Initialize hexagonal grid
for x in range(col):
    for y in range(row):
        # store neighbours of the node and define if it is rubbish room
        hex_map[(x, y)] = {'rubbish': False, 'neighbors': []}

# Define coordinates for rubbish nodes
rubbish_nodes = [
    (0, 2), (1, 4), (2, 2), (3, 2),
    (3, 5), (5, 2), (5, 4), (7, 4),
    (7, 1), (8, 5), (8, 3), (8, 1), (9,3)
]

# Define weight and volume for each rubbish node
rubbish_properties = {
    (0, 2): {'weight': 10, 'volume': 1},
    (1, 4): {'weight': 30, 'volume': 3},
    (2, 2): {'weight': 5, 'volume': 3},
    (3, 2): {'weight': 5, 'volume': 1},
    (3, 5): {'weight': 10, 'volume': 2},
    (5, 2): {'weight': 20, 'volume': 1},
    (5, 4): {'weight': 10, 'volume': 2},
    (7, 4): {'weight': 5, 'volume': 2},
    (7, 1): {'weight': 30, 'volume': 3},
    (8, 5): {'weight': 20, 'volume': 2},
    (8, 3): {'weight': 10, 'volume': 3},
    (9, 3): {'weight': 10, 'volume': 1},
    (8, 1): {'weight': 5, 'volume': 3}
}

# Update the map to mark the rubbish nodes
for node in rubbish_nodes:
    # Initialize the room contains rubbish
    hex_map[node]['rubbish'] = True
    # Update the node with its weight and size into hex_map
    hex_map[node].update(rubbish_properties[node])

# Helper function to get neighbours on a hexagonal grid
def get_neighbours(coord, hex_map):
    x, y = coord
    # 4 directions: Up, Down, Left, Right
    steps = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if x % 2 == 0:  # Adjust neighboring positions for even columns
        steps.append((1, -1))
        steps.append((-1, -1))
    else:  # Adjust neighboring positions for odd columns
        steps.append((1, 1))
        steps.append((-1, 1))

    # To store the neighbours node
    neighbours = []
    for dx, dy in steps:
        # Getting the neighbour nodes by adding "steps" to the current node
        neighbour_x = x + dx
        neighbour_y = y + dy
        if (neighbour_x, neighbour_y) in hex_map:
            # If neighbour node is valid, add into the "neighbours" list
            neighbours.append((neighbour_x, neighbour_y))
    return neighbours


# Define connections between the nodes using the new helper function
for x in range(col):
    for y in range(row):
        # Ensure each nodes has its neighbouring nodes defined
        hex_map[(x, y)]['neighbors'] = get_neighbours((x, y), hex_map)

# Define the cost function for A* search
def cost(node, goal):
    return euclidean_distance(node, goal)

# Define the heuristic function for A* search
def heuristic(node, goal):
    return euclidean_distance(node, goal)

# A* search algorithm
def a_star_search(start, goal, hex_map):
    # The open and closed sets
    # Priority queue of rooms
    open = [(0, start)]
    # Store visited neighbour
    closed = set()

    # Path reconstruction data
    g_scores = {start: 0}
    # To store the parent nodes
    came_from = {}

    while open:
        # Pop the node with the lowest cost from the open set
        current = heapq.heappop(open)[1]

        # Goal check
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            # Add to 'path' if not start to avoid duplication
            path.append(current) if current != start else None

            # Return reverised path and total cost from start to goal node
            return path[::-1], g_scores[goal]

        closed.add(current)

        # Expand the current node
        for neighbor in hex_map[current]['neighbors']:
            # If the neighbor node has been visited, skip it
            if neighbor in closed:
                continue

            # Add the cost of reaching the current node (g_cost) and the cost of moving from current node to neighbour node
            tentative_g_score = g_scores[current] + cost(current, neighbor)

            # If neighbour not in 'open' set or tentative cost lower than current g cost, means getting better path
            if neighbor not in [i[1] for i in open] or tentative_g_score < g_scores.get(neighbor, 0):
                # Now the better path will update become current node
                came_from[neighbor] = current
                # The cost will be updated
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                # The neighbour node will be added to the 'open' set with its lowest cost
                heapq.heappush(open, (f_score, neighbor))

    return None, float('inf')

# Main loop
current_position = hex_map['rubbish_bin']['start']
# Include start node in the path
path = [current_position]
total_cost = 0

# Display start node
print(f"Start Node: {current_position}\n")

# If rubbish bin is not 50 and 10
while rubbish_nodes or not rubbish_nodes and hex_map['rubbish_bin']['capacity'] != max_weight and hex_map['rubbish_bin']['volume'] != max_size:
    # Generate a list of paths and their scores
    path_list = []

    # Get the rubbish node position
    for node in rubbish_nodes:
        # Get the weight and volume of the rubbish
        rubbish_weight = hex_map[node]['weight']
        rubbish_volume = hex_map[node]['volume']
        # If rubbish weight and size smaller or equal to rubbish bin capacity
        if rubbish_weight <= hex_map['rubbish_bin']['capacity'] and rubbish_volume <= hex_map['rubbish_bin']['volume']:
            # Find the path to this node
            new_path, new_cost = a_star_search(current_position, node, hex_map)
            # Calculate the score of this path (you may change the scoring function according to your requirement)
            # In this case, the score is simply the negative of the cost - that is, lower cost paths get higher score.
            score = -new_cost
            path_list.append((score, new_path, new_cost, node, rubbish_weight, rubbish_volume))

    # If there are collectible rubbish nodes, move to the best one
    if path_list:
        print("Searching for nearest rubbish...")
        path_list.sort(reverse=True)  # Sort by score in descending order
        best_score, new_path, new_cost, closest_rubbish, rubbish_weight, rubbish_volume = path_list[0]
        path += new_path
        total_cost += new_cost
        hex_map['rubbish_bin']['capacity'] -= rubbish_weight
        hex_map['rubbish_bin']['volume'] -= rubbish_volume
        accumulated_weight = max_weight - hex_map['rubbish_bin']['capacity']
        accumulated_size = max_size - hex_map['rubbish_bin']['volume']
        rubbish_nodes.remove(closest_rubbish)
        current_position = closest_rubbish

        # Print the actual traversal nodes
        for node in new_path:
            print("Current Node:", node)

        print(f"Found rubbish!\nCollected rubbish at {closest_rubbish}")
        print(f"Accumulated collected rubbish weight: {accumulated_weight} kg")
        print(f"Accumulated collected rubbish size: {accumulated_size} m\u00B3")
    else:
        # If there are no collectible rubbish nodes, move to the closest disposal room
        print("Rubbish bin is full\nSearching for nearest disposal room...")
        closest_disposal = min(disposal_rooms, key=lambda node: euclidean_distance(current_position, node))
        new_path, new_cost = a_star_search(current_position, closest_disposal, hex_map)
        path += new_path

        # Print the actual traversal nodes
        for node in new_path:
            print("Current Node:", node)

        total_cost += new_cost
        current_total_weight = max_weight - hex_map['rubbish_bin']['capacity']
        current_total_size = max_size - hex_map['rubbish_bin']['volume']
        hex_map['rubbish_bin']['capacity'] = max_weight
        hex_map['rubbish_bin']['volume'] = max_size
        print(f"Rubbish of total weight {current_total_weight} kg and total size of {current_total_size} m\u00B3 disposed at {closest_disposal}")
        current_position = closest_disposal

    print("")

print("All rubbish cleared\n")
print("Path:", path)
cost = len(path)
print("\nTotal Cost: ", cost)

# Call the create_gui function to create the GUI
create_gui(hex_map, path, max_weight, max_size)

# End the timer
end_time = time.time()

# Calculate the execution time in seconds
execution_time = end_time - start_time

# Display the execution time
print(f"\nExecution time: {execution_time:.2f} seconds")