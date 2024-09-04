import random

# Define the environment size (typically 4x4 grid)
GRID_SIZE = 4

# Define elements in the Wumpus World
EMPTY = 0
PIT = 1
WUMPUS = 2
GOLD = 3

# Define percepts
BREEZE = 'Breeze'
STENCH = 'Stench'
GLITTER = 'Glitter'


# Define the Wumpus World Environment
class WumpusWorld:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.agent_position = (GRID_SIZE - 1, 0)  # Agent starts at the bottom-left corner
        self.agent_alive = True
        self.has_gold = False

        # Place Wumpus, pits, and gold randomly
        self._place_element(WUMPUS)
        self._place_element(GOLD)
        for _ in range(3):  # Let's assume there are 3 pits in the grid
            self._place_element(PIT)

    def _place_element(self, element):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.grid[x][y] == EMPTY and (x, y) != self.agent_position:
                self.grid[x][y] = element
                break

    def get_percepts(self):
        x, y = self.agent_position
        percepts = []

        # Check for adjacent cells for breeze or stench
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.grid[nx][ny] == PIT:
                    percepts.append(BREEZE)
                if self.grid[nx][ny] == WUMPUS:
                    percepts.append(STENCH)

        # Check for gold in the current cell
        if self.grid[x][y] == GOLD:
            percepts.append(GLITTER)

        return percepts

    def move_agent(self, direction):
        if not self.agent_alive:
            print("The agent is dead. Game over!")
            return

        x, y = self.agent_position
        if direction == "UP" and x > 0:
            x -= 1
        elif direction == "DOWN" and x < GRID_SIZE - 1:
            x += 1
        elif direction == "LEFT" and y > 0:
            y -= 1
        elif direction == "RIGHT" and y < GRID_SIZE - 1:
            y += 1
        else:
            print("Invalid move")
            return

        self.agent_position = (x, y)
        self._check_current_position()

    def _check_current_position(self):
        x, y = self.agent_position
        if self.grid[x][y] == WUMPUS:
            print("Agent was eaten by the Wumpus!")
            self.agent_alive = False
        elif self.grid[x][y] == PIT:
            print("Agent fell into a pit!")
            self.agent_alive = False
        elif self.grid[x][y] == GOLD:
            print("Agent found the gold!")
            self.has_gold = True
            self.grid[x][y] = EMPTY

    def display_grid(self):
        print("Wumpus World Grid:")
        for row in self.grid:
            print(row)
        print("Agent Position:", self.agent_position)


# Define the Agent's behavior
class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.alive = True

    def perceive_and_act(self):
        while self.alive:
            percepts = self.world.get_percepts()
            print("Percepts:", percepts)

            if GLITTER in percepts:
                print("Gold found! Grabbing the gold and exiting the game.")
                self.world.move_agent("EXIT")
                break

            # Simple random exploration strategy
            moves = ["UP", "DOWN", "LEFT", "RIGHT"]
            move = input()
            print("Agent moving", move)
            self.world.move_agent(move)

            if not self.world.agent_alive:
                self.alive = False
                print("Agent died. Game over.")
                break


# Simulate the Wumpus World Problem
world = WumpusWorld()
agent = WumpusAgent(world)

# Display the initial state
world.display_grid()

# Run the agent in the environment
agent.perceive_and_act()
