import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
from scipy.sparse.csgraph import minimum_spanning_tree


def heuristic(closedList, adj_matrix):
    remaining_cities = [i for i in range(len(adj_matrix)) if i not in closedList]
    if len(remaining_cities) < 2:
        return 0

    graph = np.full((len(adj_matrix), len(adj_matrix)), np.inf)
    for i in remaining_cities:
        for j in remaining_cities:
            if i != j:
                graph[i, j] = adj_matrix[i, j]
    mst = minimum_spanning_tree(graph).toarray()
    return mst[mst > 0].sum() / 2


def check_consistency(node, neighbor, cost, h_current, distance_matrix):
    h_neighbor = heuristic(node + [neighbor], distance_matrix)
    edge_cost = distance_matrix[node[-1]][neighbor]
    return h_current <= edge_cost + h_neighbor


def a_star_algorithm(start, goal, adj_matrix):
    n = len(adj_matrix)
    heapqueue = [(0, start, [start], 0)]  # (f_value, current_node, path, cost)
    visited = set()
    best_cost = {start: 0}
    path_history = []

    while heapqueue:
        f_value, current_node, path, cost = heapq.heappop(heapqueue)
        visited.add(current_node)
        path_history.append((list(path), current_node))  # Track path history
        print(path_history)
        if current_node == goal:
            return path, cost, path_history

        for neighbor in range(n):
            if adj_matrix[current_node][neighbor] > 0 and neighbor not in visited:
                new_cost = cost + adj_matrix[current_node][neighbor]
                new_path = path + [neighbor]
                h_value = heuristic(new_path, adj_matrix)
                if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                    best_cost[neighbor] = new_cost
                    if check_consistency(path, neighbor, new_cost, h_value, adj_matrix):
                        heapq.heappush(heapqueue, (new_cost + h_value, neighbor, new_path, new_cost))

    return None, float('inf'), path_history  # No path found


def animate_a_star(distance_matrix, start_node, goal_node, node_positions):
    # Run the A* algorithm to get the path, cost, and the history of the search
    path, cost, path_history = a_star_algorithm(start_node, goal_node, distance_matrix)

    fig, ax = plt.subplots()
    ax.set_title('A* Algorithm Animation')
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)

    # Plot the nodes as points in 2D space
    for i, (x, y) in enumerate(node_positions):
        ax.plot(x, y, 'bo', markersize=10)
        ax.text(x, y + 0.2, f'{i}', ha='center')

    # Draw the edges based on the adjacency matrix
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix)):
            if distance_matrix[i][j] > 0:
                x_values = [node_positions[i][0], node_positions[j][0]]
                y_values = [node_positions[i][1], node_positions[j][1]]
                ax.plot(x_values, y_values, 'gray')

    def update(frame):
        ax.clear()

        # Plot the nodes and display their heuristic values
        for i, (x, y) in enumerate(node_positions):
            ax.plot(x, y, 'bo', markersize=10)
            ax.text(x, y + 0.2, f'{i}', ha='center')

        # Redraw the edges
        for i in range(len(distance_matrix)):
            for j in range(len(distance_matrix)):
                if distance_matrix[i][j] > 0:
                    x_values = [node_positions[i][0], node_positions[j][0]]
                    y_values = [node_positions[i][1], node_positions[j][1]]
                    ax.plot(x_values, y_values, 'gray')

        # Highlight the traversed path up to the current frame and show the heuristic values
        for (path, current_node) in path_history[:frame + 1]:
            for i in range(1, len(path)):
                x_values = [node_positions[path[i - 1]][0], node_positions[path[i]][0]]
                y_values = [node_positions[path[i - 1]][1], node_positions[path[i]][1]]
                ax.plot(x_values, y_values, 'r', linewidth=2)

            # Show the heuristic value next to the current node
            heuristic_value = heuristic(path, distance_matrix)
            ax.text(node_positions[current_node][0], node_positions[current_node][1] - 0.3,
                    f'h={heuristic_value:.2f}', ha='center', color='green', fontsize=10)

        # If we have reached the goal, display the final path and cost
        if frame == len(path_history) - 1:
            ax.set_title(f'Path Reached! Total Cost: {cost:.2f}', fontsize=14, color='green')
            for i in range(1, len(path)):
                x_values = [node_positions[path[i - 1]][0], node_positions[path[i]][0]]
                y_values = [node_positions[path[i - 1]][1], node_positions[path[i]][1]]
                ax.plot(x_values, y_values, 'b', linewidth=3)  # Final path in blue

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(path_history), repeat=True, interval=1000)
    plt.show()


# Function to take matrix input and positions for nodes
def take_user_input():
    # Input number of locations
    n = int(input("Enter the number of locations (nodes): "))

    # Input adjacency matrix
    print(f"Enter the {n}x{n} adjacency matrix (use space to separate values):")
    adj_matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        adj_matrix.append(row)

    adj_matrix = np.array(adj_matrix)

    # Input start and goal nodes
    start_node = int(input("Enter the start node (0-indexed): "))
    goal_node = int(input("Enter the goal node (0-indexed): "))

    # Input positions for nodes in 2D plane
    print(f"Enter the x, y coordinates for each of the {n} nodes (separated by space):")
    node_positions = []
    for _ in range(n):
        x, y = map(float, input().split())
        node_positions.append((x, y))

    return adj_matrix, start_node, goal_node, node_positions


# Example usage
if __name__ == "__main__":
    distance_matrix, start_node, goal_node, node_positions = take_user_input()
    animate_a_star(distance_matrix, start_node, goal_node, node_positions)


'''
7

0 2 0 1 0 0 0
2 0 3 2 0 0 0 
0 3 0 0 0 0 4 
1 2 0 0 5 0 0
0 0 0 5 0 2 3 
0 0 0 0 2 0 1
0 0 4 0 3 1 0 

0
6

1 1 
2 3 
5 4 
1 5 
3 7 
6 7 
8 5

'''