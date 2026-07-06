import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import heapq
import math

def astar(grid, start, end):
    """
    Finds the shortest path from start to end using the A* algorithm.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # --- Helper Function: Heuristic ---
    # We use Euclidean distance as the heuristic (h-cost)
    def heuristic(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    # --- Data Structures ---
    # Priority queue (min-heap) to store (f_cost, node)
    # This lets us always get the node with the lowest f_cost
    open_set = []
    heapq.heappush(open_set, (0, start)) # (f_cost, node)

    # came_from[node] = previous_node
    # Used to reconstruct the path once we reach the end
    came_from = {}
    
    # g_cost[node] = cost from start to node
    # Initialize all costs to infinity
    g_cost = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    g_cost[start] = 0

    # f_cost[node] = g_cost + heuristic
    # Initialize all costs to infinity
    f_cost = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    f_cost[start] = heuristic(start, end)
    
    # --- Main A* Loop ---
    while open_set:
        # Get the node in the open set with the lowest f_cost
        # current_f, current_node = heapq.heappop(open_set)
        # We only need the node. The f_cost is stored in the f_cost dict.
        current_node = heapq.heappop(open_set)[1]

        # --- Goal Reached ---
        if current_node == end:
            # Reconstruct and return the path
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1] # Return reversed path (start to end)

        # --- Check Neighbors ---
        # We check all 8 directions (including diagonals)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            neighbor = (current_node[0] + dr, current_node[1] + dc)
            
            # Check if neighbor is within bounds
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
                
            # Check if neighbor is an obstacle (1 = obstacle)
            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            # --- Calculate Path Cost ---
            # Cost to move to neighbor is 1 for straight, sqrt(2) for diagonal
            move_cost = math.sqrt(dr**2 + dc**2)
            tentative_g_cost = g_cost[current_node] + move_cost

            # If this path to the neighbor is better than any previous one
            if tentative_g_cost < g_cost[neighbor]:
                # This is a better path, so record it
                came_from[neighbor] = current_node
                g_cost[neighbor] = tentative_g_cost
                f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, end)
                
                # Add neighbor to the open set to be evaluated
                # We use a tuple (f_cost, node) for the heap
                heapq.heappush(open_set, (f_cost[neighbor], neighbor))

    # If the loop finishes and we never reached the end, no path exists
    return None

def visualize_path(grid, path, start, end):
    """
    Uses Matplotlib to draw the grid, obstacles, and path.
    """
    # --- Create a numeric grid for plotting ---
    # 0 = Empty (white)
    # 1 = Obstacle (black)
    # 2 = Start (green)
    # 3 = End (red)
    # 4 = Path (orange)
    
    plot_grid = [row[:] for row in grid] # Make a copy
    
    if path:
        for (r, c) in path:
            if (r, c) != start and (r, c) != end:
                plot_grid[r][c] = 4 # Path
                
    plot_grid[start[0]][start[1]] = 2 # Start
    plot_grid[end[0]][end[1]] = 3 # End

    # --- Define colors ---
    # 0:white, 1:black, 2:green, 3:red, 4:orange
    cmap = mcolors.ListedColormap(['white', 'black', '#4CAF50', '#F44336', '#FF9800'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # --- Plot the grid ---
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(plot_grid, cmap=cmap, norm=norm)

    # Draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.5)
    ax.set_xticks(range(len(grid[0])))
    ax.set_yticks(range(len(grid)))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Set ticks to be in the center of the cells
    ax.set_xticks([x - 0.5 for x in range(1, len(grid[0]))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(grid))], minor=True)
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=0.5)

    plt.title("A* Pathfinding Visualization")
    plt.show()

# --- Main Program ---

# Define the sample map (the grid)
# 0 = Walkable path
# 1 = Obstacle (wall/building)
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Define start and end points
# Format is (row, col)
start_point = (1, 1)
end_point = (10, 13)

# --- Run the algorithm and visualize ---
found_path = astar(grid, start_point, end_point)

if found_path:
    print(f"Path found! Length: {len(found_path)}")
else:
    print("No path found.")

visualize_path(grid, found_path, start_point, end_point)