import pygame
import random

CELL_SIZE = 5
WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600

# Simulation parameters
PROBA_COW_INIT = 10
PROBA_GRASS_INIT = 40
COW_ENERGY_INIT = 4
COW_ENERGY_TO_MAKE_BABY = 5
COW_LOSS_ENERGY_STEP = 1
COW_INCREASE_ENERGY_EAT = 2
PROBA_GRASS_GROW = 10
TICK = -1

def main():
    pygame.init()

    # Create map
    game_map = generate_map()

    # Create window
    window = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    # New map
                    game_map = generate_map()
        
        # Display map
        display_map(game_map, window)

        # Advance to next iteration
        next_iteration(game_map)


        # Check if only grass exists
        if check_if_only_grass(game_map):
            # Regenerate map
            game_map = generate_map()

        pygame.time.wait(TICK)
        
    pygame.quit()

def check_if_only_grass(game_map):
    """
    Check if only grass exists on the map
    """
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            if game_map[y][x] != 1:
                return False
    return True

def next_iteration(game_map):
    """
    Perform one iteration step
    """
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            # Check if cow or grass
            if not isinstance(game_map[y][x], Cow) and game_map[y][x] != 1:
                continue

            # Check if cow
            if isinstance(game_map[y][x], Cow):
                # Make baby
                if game_map[y][x].can_make_baby():
                    direction_baby = random.randint(0, 3)
                    is_free = check_free_place(game_map, y, x, direction_baby)

                    if is_free == 0 or is_free == 1:
                        if direction_baby == 0:
                            # Up
                            game_map[y-1][x] = Cow()
                        if direction_baby == 1:
                            # Right
                            game_map[y][x+1] = Cow()
                        if direction_baby == 2:
                            # Down
                            game_map[y+1][x] = Cow()
                        if direction_baby == 3:
                            # Left
                            game_map[y][x-1] = Cow()

                # Move cow
                game_map[y][x].reduce_energy()
                if game_map[y][x].no_energy():
                    game_map[y][x] = 0
                    continue

                direction = random.randint(0, 3)
                item = check_free_place(game_map, y, x, direction)

                # move if not blocked or a cow
                if item != -1 and item != 2:
                    if item == 1:
                        game_map[y][x].increase_energy()
                    if direction == 0:
                        game_map[y-1][x] = game_map[y][x]
                    if direction == 1:
                        game_map[y][x+1] = game_map[y][x]
                    if direction == 2:
                        game_map[y+1][x] = game_map[y][x]
                    if direction == 3:
                        game_map[y][x-1] = game_map[y][x]
                    game_map[y][x] = 0
                
                            
            # Check if grass
            if game_map[y][x] == 1:
                if random.randint(1, 100) <= PROBA_GRASS_GROW: 
                    direction = random.randint(0, 3)
                    item = check_free_place(game_map, y, x, direction)

                    if item == 0:
                        if direction == 0:
                            game_map[y-1][x] = 1
                        if direction == 1:
                            game_map[y][x+1] = 1
                        if direction == 2:
                            game_map[y+1][x] = 1
                        if direction == 3:
                            game_map[y][x-1] = 1


def check_free_place(game_map, y, x, direction):
    """
    Check if place is free
    """

    # Up
    if direction == 0:
        if y == 0:
            return -1
        if game_map[y-1][x] == 0:
            return 0
        if game_map[y-1][x] == 1:
            return 1
        if isinstance(game_map[y-1][x], Cow):
            return 2
    
    # Right
    if direction == 1:
        if x == len(game_map[0]) - 1:
            return -1
        if game_map[y][x+1] == 0:
            return 0
        if game_map[y][x+1] == 1:
            return 1
        if isinstance(game_map[y][x+1], Cow):
            return 2

    # Down
    if direction == 2:
        if y == len(game_map) - 1:
            return -1
        if game_map[y+1][x] == 0:
            return 0
        if game_map[y+1][x] == 1:
            return 1
        if isinstance(game_map[y+1][x], Cow):
            return 2

    # Left
    if direction == 3:
        if x == 0:
            return -1
        if game_map[y][x-1] == 0:
            return 0
        if game_map[y][x-1] == 1:
            return 1
        if isinstance(game_map[y][x-1], Cow):
            return 2

def display_map(game_map, window):
    """
    Display the map
    """

    # Clear screen
    window.fill((0, 0, 0))

    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            if isinstance(game_map[y][x], Cow):
                pygame.draw.rect(window, (255, 255, 255), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if game_map[y][x] == 1:
                pygame.draw.rect(window, (0, 255, 0), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

def generate_map():
    """
    Generate map
    """

    game_map = []
    for i in range(HEIGHT_SCREEN // CELL_SIZE):
        sub_map = []
        for j in range(WIDTH_SCREEN // CELL_SIZE):
            sub_map.append(generate_item())
        game_map.append(sub_map)

    return game_map

def generate_item():
    """
    Generate an item: cow, grass, or nothing
    """
    if PROBA_COW_INIT + PROBA_GRASS_INIT > 100:
        raise ValueError("The sum of the probabilities of cows and grass must be less than 100")

    rand_num = random.randint(1, 100)
    if 0 < rand_num <= PROBA_COW_INIT:
        return Cow()
    
    if PROBA_COW_INIT < rand_num <= PROBA_COW_INIT + PROBA_GRASS_INIT:
        return 1
    
    return 0

class Cow:
    def __init__(self):
        self.energy = COW_ENERGY_INIT

    def can_make_baby(self):
        return self.energy >= COW_ENERGY_TO_MAKE_BABY
    
    def reduce_energy(self):
        self.energy -= COW_LOSS_ENERGY_STEP
    
    def no_energy(self):
        return self.energy <= 0

    def increase_energy(self):
        self.energy += COW_INCREASE_ENERGY_EAT

main()