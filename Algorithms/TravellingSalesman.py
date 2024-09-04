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
    n = int(input("enter the number of cities\n"))
    adj_matrix = np.zeros((n, n))
    i = 0
    while i < n:
        j = 0
        while j < n:
            print("distance between", i,"and", j)
            x = int(input())
            if x >= 0:
                adj_matrix[i, j] = x
                j += 1
            else:
                print("INVALID INPUT TRY AGAIN")
                continue
        i += 1

    best_tour, min_cost = tsp_branch_and_bound(adj_matrix)
    en = time.perf_counter()
    print("Best Tour:", best_tour)
    print("Minimum Cost:", min_cost)
    print((en - st) * (10 ** 6), "microsecond")
