import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
import heapq


def heuristic(nodelist, adj_matrix):
    remaining_cities = [i for i in range(len(adj_matrix)) if i not in nodelist]
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

    while heapqueue:
        print(best_cost)
        # Extract the node with the minimum f_value
        f_value, current_node, path, cost = heapq.heappop(heapqueue)

        visited.add(current_node)
        print("visited  : ", visited)

        if current_node == goal:
            return path, cost



        for neighbor in range(n):
            print("entering " , neighbor)
            if adj_matrix[current_node][neighbor] > 0 and neighbor not in visited:
                new_cost = cost + adj_matrix[current_node][neighbor]
                new_path = path + [neighbor]
                h_value = heuristic(new_path, adj_matrix)
                print("heap before push:", heapqueue)
                if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                    best_cost[neighbor] = new_cost
                    print(best_cost," best cost after updation")
                    # Check consistency of the heuristic
                    if check_consistency(path, neighbor, new_cost, h_value, adj_matrix):

                        heapq.heappush(heapqueue, (new_cost + h_value, neighbor, new_path, new_cost))
                        print("heap after push:"  ,heapqueue)
    return None, float('inf')  # No path found


distance_matrix = np.array([[0, 1, 4, 6],
                            [1, 0, 2, 5],
                            [4, 2, 0, 3],
                            [6, 5, 3, 0]])

start_node = 0
goal_node = 3

path, cost = a_star_algorithm(start_node, goal_node, distance_matrix)
print("Path:", path)
print("Cost:", cost)
