# Hill Climbing Algorithm for Taxi Routing
def hill_climbing_route(adj_matrix, start, end):
    n = len(adj_matrix)
    current_location = start
    current_route = [current_location]
    total_cost = 0

    while current_location != end:
        next_location = None
        min_cost = float('inf')

        # Check all possible next locations
        for neighbor in range(n):
            if neighbor not in current_route and adj_matrix[current_location][neighbor] != -1:
                cost = adj_matrix[current_location][neighbor]
                cost = objective_function(cost)
                if cost < min_cost:
                    min_cost = cost
                    next_location = neighbor

        if next_location is None:  # No valid next location found
            break

        # Update the current route and total cost
        current_route.append(next_location)
        total_cost += min_cost
        current_location = next_location

    return current_route, -1*total_cost


# Calculate the total cost of a given route
def objective_function(x):
    return -1*(x**2) + 4 * x  # Example: f(x) = -x^2 + 4x (a downward-opening parabola)


# Get a valid adjacency matrix from the user
def get_adjacency_matrix(n):
    print(f"Enter the adjacency matrix for {n} locations (enter -1 for no connection):")
    adj_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            while True:
                value = float(input(f"Value for {i} to {j} (negative/0 is invalid): "))
                if value > 0 or value == -1:  # -1 indicates no connection
                    row.append(value)
                    break
                else:
                    print("Invalid value. Please enter a positive value or -1 for no connection.")
        adj_matrix.append(row)
    return adj_matrix


# Example usage
if __name__ == "__main__":
    n = int(input("Enter the number of locations: "))
    adj_matrix = get_adjacency_matrix(n)

    start = 0  # Assuming the start location is always 0
    end = n - 1  # Assuming the end location is always the last location

    best_route, total_cost = hill_climbing_route(adj_matrix, start, end)
    print(f"Optimal route: {' -> '.join(map(str, best_route))}, Total cost: {total_cost:.2f}")
