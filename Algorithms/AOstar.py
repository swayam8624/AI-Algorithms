from collections import deque


class Node:
    def __init__(self, name, is_goal=False, is_and_node=False):
        self.name = name
        self.is_goal = is_goal
        self.is_and_node = is_and_node
        self.children = []
        self.parent = None
        self.cost = float('inf')
        self.heuristic = 0
        self.value = float('inf')


def ao_star(start, goals):
    open_list = deque([start])
    visited = set()
    all_paths = []  # To store all valid paths

    while open_list:
        current = open_list.popleft()
        if current in visited:
            continue

        visited.add(current)

        if all(goal in visited for goal in goals):
            all_paths.append(reconstruct_path(current))
            continue  # Continue to find other paths

        for child in current.children:
            if child not in visited:
                child.cost = min(child.cost, current.cost + 1)
                child.heuristic = calculate_heuristic(child, goals, visited)
                child.value = child.cost + child.heuristic

                if child not in open_list:
                    open_list.append(child)

        # Ensure all paths are explored by not stopping early
        open_list = deque(sorted(open_list, key=lambda node: node.value))

    return all_paths if all_paths else None


def calculate_heuristic(node, goals, closed_list):
    if node.is_and_node:
        return sum(1 for child in node.children if child not in closed_list and child.is_goal)
    else:
        return len([goal for goal in goals if goal not in closed_list])


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.name)
        node = node.parent
    return path[::-1]


# Example usage:
# Define nodes
start = Node('Start')
child1 = Node('Child1')
goal2 = Node('Goal2', is_goal=True)
goal1 = Node('Goal1', is_goal=True)

# Define relationships
start.children = [goal1, goal2, child1]
child1.children = [goal1]
goal2.parent = start
goal1.parent = child1
child1.parent = start

# Define goals list
goals = [goal1, goal2]

paths = ao_star(start, goals)
print("Paths found:", paths)
