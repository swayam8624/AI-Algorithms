import numpy as np
import time


# Function to calculate the lower bound of the path cost
def calculate_lower_bound(matrix, n):
    lower_bound = 0
    for i in range(n):
        min_cost = np.min(matrix[i][np.nonzero(matrix[i])])
        if min_cost == 0:
            min_cost = float('inf')
        lower_bound += min_cost
    return lower_bound


# Function to calculate the total distance of a tour
def calculate_tour_distance(tour, distance_matrix):
    distance = 0
    for i in range(len(tour) - 1):
        distance += distance_matrix[tour[i], tour[i + 1]]
    distance += distance_matrix[tour[-1], tour[0]]  # Return to the starting city
    return distance


# Function to implement the branch and bound
def tsp_branch_and_bound(distance_matrix):
    n = distance_matrix.shape[0]
    min_cost = float('inf')
    best_tour = []

    def solve(current_city, count, cost, tour, lower_bound):
        nonlocal min_cost, best_tour

        if count == n and distance_matrix[current_city][0] > 0:
            total_cost = cost + distance_matrix[current_city][0]
            if total_cost < min_cost:
                min_cost = total_cost
                best_tour = tour + [0]
            return

        for i in range(n):
            if distance_matrix[current_city][i] > 0 and i not in tour:
                temp_cost = cost + distance_matrix[current_city][i]
                temp_lower_bound = lower_bound + distance_matrix[current_city][i]

                # Prune branches if the lower bound is not promising
                if temp_lower_bound < min_cost:
                    solve(i, count + 1, temp_cost, tour + [i], temp_lower_bound)

    lower_bound = calculate_lower_bound(distance_matrix, n)
    solve(0, 1, 0, [0], lower_bound)
    return best_tour, min_cost


if __name__ == "__main__":
    st = time.perf_counter()
    adj_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])

    best_tour, min_cost = tsp_branch_and_bound(adj_matrix)
    en = time.perf_counter()
    print("Best Tour:", best_tour)
    print("Minimum Cost:", min_cost)
    print((en - st)*(10**6),"microsecond")
