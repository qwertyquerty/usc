import heapq
import math
import pygame

MAP_IMAGE = "map.png"
DRAW_INTERVAL = 1000

LEGAL_STEPS = [(0, 2), (2, 0), (0, -2), (-2, 0),(2, 2), (-2, -2), (2, -2), (-2, 2),  (1, 2), (2, 1), (-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1)]

START = (386, 868) # Parkside
END = (783, 458) # EVK

WALL = (0,0,0)


pygame.init()

grid = pygame.image.load(MAP_IMAGE)

screen = pygame.display.set_mode(grid.get_size(), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
display = pygame.Surface(grid.get_size())
searched = pygame.Surface(grid.get_size())

grid.convert() # Optimizes surface for fast blitting

pygame.font.init()
pygame.display.set_caption("Path Optimizer")

font = pygame.font.SysFont('Courier', 12)

clock = pygame.time.Clock()

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.parent = None
        
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

def heuristic(a, b):
    # City block distance with cartesian distance for ordering
    return (abs(a.x-b.x)+abs(a.y-b.y)) + (math.sqrt((a.x-b.x)**2+(a.y-b.y)**2))/1000

start = Node(*START)
end = Node(*END)

node_queue = [] # Nodes we will eventually visit (heap)
transposition_table = {} # Nodes we have already visited

completed = 0
pruned = 0
nodes = 0

heapq.heappush(node_queue, start)

best_length = None
best_path = None

while True:
    if len(node_queue):
        current = heapq.heappop(node_queue)
        
        if current.x == end.x and current.y == end.y:
            # We completed a new path

            if not best_length or current.g < best_length:
                # The new path is the new best path         
                best_length = current.g

                path = []
                while current.parent:
                    path.append((current.x, current.y))
                    current = current.parent
                
                path.append((current.x, current.y))

                best_path = path

                print(f"{nodes}\tNew Best\t{round(best_length, 1)}")

            completed += 1

        # Update transposition table
        transposition_table[(current.x,current.y)] = current.g

        # Mark this node as searched
        searched.set_at((current.x, current.y), (64, 0, 0))

        if not best_length or (current.g+math.sqrt((current.x-end.x)**2+(current.y-end.y)**2)) < best_length: # futility pruning
            # Iterate throguh neighbors
            for dx, dy in LEGAL_STEPS:
                x = current.x + dx
                y = current.y + dy
                
                # Out of bounds or wall
                if x < 0 or x >= grid.get_size()[0] or y < 0 or y >= grid.get_size()[1] or grid.get_at((x, y)) == WALL:
                    continue
                    
                neighbor = Node(x, y)
                neighbor.g = current.g + math.sqrt((dx**2)+(dy**2))
                neighbor.h = heuristic(neighbor, end)
                neighbor.parent = current

                # transposition pruning
                if (x, y) in transposition_table and transposition_table[(x, y)] <= neighbor.g:
                    pruned += 1
                    continue
                
                # Add the neighbor to the queue
                heapq.heappush(node_queue, neighbor)
        else:
            pruned += 1
        
        nodes += 1

    if nodes % DRAW_INTERVAL == 0 or len(node_queue) == 0:
        # Draw the map (color inverted)
        display.fill((255,255,255))
        display.blit(grid, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Color the pixels we've searched
        display.blit(searched, (0,0), None, pygame.BLEND_RGBA_ADD)

        # Draw direct line from end of current path to goal to visualize futility pruning
        pygame.draw.line(display, (128,0,128), (current.x, current.y), (end.x, end.y))

        # Draw current path
        c = current
        while c is not None:
            a = c
            b = c
            c = c.parent
            if c == None: break
            else:
                b = c
            pygame.draw.line(display, (255,0,0), (a.x, a.y), (b.x, b.y))
        
        if best_path:
            # If we found a best path, draw it
            c = 0
            while c < len(best_path):
                pygame.draw.line(display, (0,255,0), best_path[c], best_path[min(c+1, len(best_path)-1)])
                c += 1

        # Text rendering
        text = font.render(f"Searched: {nodes}", False, (255,255,255))
        display.blit(text, (2,2))

        text = font.render(f"Completed: {completed}", False, (255,255,255))
        display.blit(text, (2,16))

        text = font.render(f"Pruned: {pruned}", False, (255,255,255))
        display.blit(text, (2,30))

        text = font.render(f"Best: {round(best_length, 1) if best_length else 'None'}", False, (255,255,255))
        display.blit(text, (2,44))

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        # Draw the display to the screen and update the screen
        screen.blit(display, (0,0))
        pygame.display.flip()
