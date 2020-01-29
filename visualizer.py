import pygame
from pygame.locals import *
from copy import deepcopy
from node import Node

# initial grid and starting position
grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# we can define constants
TITLE_OFFSET = 70

WIDTH = 50
HEIGHT = 50
MARGIN = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
FORREST_GREEN = (34, 139, 34)
LIME_GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
BLUE = (0,255,255)
RED = (255, 0, 0)

   

start_pos = (0,0)
end_pos = (9,9)
# the mode can be settign the end point(1), setting the starting point(2), setting walls(3) and solving(4)
mode = 1
solve = False
screen = None

#variables for solving the grid
open_list = None
closed_list = None
start_node = None
end_node = None

current_solving_node = None
current_solving_children = None

solved_path = None


def draw_path(path):
    global grid, mode, start_pos, end_pos
    for block in path:
        grid[block[0]][block[1]] = 2


def draw_square(color, x , y):
    pygame.draw.rect(screen,
                    color,
                    [(MARGIN + WIDTH) * x + MARGIN,
                    (MARGIN + HEIGHT) * y + MARGIN + TITLE_OFFSET,
                    WIDTH,
                    HEIGHT])

def draw_text(text, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', 12  ) 
    text = font.render(text, True, color) 
    rec = text.get_rect()
    rec.center = (x,y)
    screen.blit(text, rec)

def initiate_solving():
    global start_node, end_node, open_list, closed_list, solve

    start_node = Node(None, (start_pos[1], start_pos[0]))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, (end_pos[1], end_pos[0]))
    end_node.g = end_node.h = end_node.f = 0
    
    open_list = []
    closed_list = []

    open_list.append(start_node)
    solve = True

# This will run through a single round of maze solving
def one_round():
    global start_node, end_node, open_list, closed_list, current_solving_children, current_solving_node, solved_path

    if len(open_list) == 0:
        return False
    # First we find the queued node with the lowest f score
    current_node = open_list[0]
    current_index = 0
    for index, item in enumerate(open_list):
        if item.f < current_node.f:
            current_node = item
            current_index = index

    # Pop current off open list, add to closed list
    open_list.pop(current_index)
    closed_list.append(current_node)

    if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            solved_path = path[::-1]
            return False

    current_solving_node = (current_node.position[1], current_node.position[0])
    # Generate children
    children = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

        # Get node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure within range
        if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0:
            continue

        # Make sure walkable terrain
        if grid[node_position[0]][node_position[1]] != 0:
            continue

        # Create new node
        new_node = Node(current_node, node_position)

        # Append
        children.append(new_node)

    # Loop through children. Frst delete the children list
    current_solving_children = []

    for child in children:
        add = True
        # Child is on the closed list
        for closed_child in closed_list:
            if child == closed_child:
                add = False
                continue

        # Create the f, g, and h values
        child.g = current_node.g + 1
        child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
        child.f = child.g + child.h

        # Child is already in the open list
        for open_node in open_list:
            if child == open_node:
                if child.g < open_node.g:
                    open_node.g = child.g
                add = False
                continue

            # if child == open_node and child.g > open_node.g:
            #     continue

        # Add the child to the open list
        if add:
            current_solving_children.append((child.position[1], child.position[0]))
            open_list.append(child)

    pygame.time.wait(500)
    return True

def main():
    global mode, grid, start_pos, end_pos, solve, current_solving_children, current_solving_node, open_list, closed_list, solved_path, screen
    # Initialise screen
    main_loop = False
    pygame.init()
    screen = pygame.display.set_mode((525, 600))
    pygame.display.set_caption('A* Visualizer')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()


    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_q]:
                    pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # gets columns and rows for object grid selection
                column = pos[0] // (WIDTH + MARGIN)
                row = (pos[1] - TITLE_OFFSET) // ( HEIGHT + MARGIN )
                if column >= 0 and column <= 9 and row <= 9 and row >= 0:
                    if mode == 0:
                        grid[row][column] = 1
                    if mode == 1:
                        #reset the old start point and set the new one
                        start_pos = (column, row)
                    if mode == 2:
                        end_pos = (column, row)

                # sets a mode if one of the rectangles are clicked on
                if pos[1] >= 10 and pos[1] <= 60: 
                    new_mode = pos[0] // (WIDTH + 10)
                    if new_mode <= 3 or new_mode >= 0:
                        mode = new_mode
                        solved_path = None

                    if mode == 3:
                        initiate_solving()

        if solve:
            if not(one_round()):
                solve = False
                current_solving_children = None
                current_solving_node = None
                open_list = None
                closed_list = None
       
        #draw the grid
        for row in range(10):
            for column in range(10):
                if grid[row][column] == 0:
                    color = WHITE
                elif grid[row][column] == 1:
                    color = RED
                elif grid[row][column] == 2:
                    color = GREEN
                else:
                    color = WHITE
                draw_square(color, column, row)
                
        # draw the starting and ending points
        draw_square(BLUE, start_pos[0], start_pos[1])
        draw_square(YELLOW, end_pos[0], end_pos[1])


        # draw the selection buttons
        for i in range(4):
            if i == mode:
                color = GREEN
            else:
                color = WHITE
            pygame.draw.rect(screen,
                color,
                [(10 + WIDTH) * i + 10,
                10 ,
                WIDTH,
                HEIGHT])

        #draw the text on each solection button
        draw_text('WALL', RED, 35 , 35)
        draw_text('START', RED, 95 , 35)
        draw_text('END', RED, 155 , 35)
        draw_text('SOLVE', RED, 215 , 35)
        
        

        # draw the visited nodes in the closed list
        if closed_list is not None:
            for i in closed_list:
                draw_square(LIME_GREEN, i.position[1], i.position[0])
               
        # draw the nodes being solved and their children
        if current_solving_children is not None:
            for i in current_solving_children:
                draw_square(FORREST_GREEN, i[0], i[1])
                
        if current_solving_node is not None:
            draw_square(DARK_GREEN, current_solving_node[0], current_solving_node[1])

        #draws the solved path
        if solved_path is not None:
            for i in solved_path:
                draw_square(GREEN, i[1], i[0])
        
        pygame.display.flip()


if __name__ == '__main__': main()