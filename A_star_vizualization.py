
from hashlib import scrypt

from pygame.draw import rect
from pygame.time import Clock
from chessMain import DIMENSION, SQ_SIZE
import pygame
from time import sleep
import math

WIDTH = HEIGHT = 800
DIMENSION = 20
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15

class Node():
    def __init__(self, position = None, parent = None, isBarrier = None):
        self.position = position
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

def main():

    board = [[0 for i in range(DIMENSION)] for j in range(DIMENSION)]
    print(len(board))
    ## Pygame initialization things
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    #screen.fill(pygame.Color("white"))
    pygame.display.set_caption("A* Pathfinding algorithm")
    

    # path reconstruction help variables
    i = 0
    ii = 0
    j = 0 
    boolen_flag_first = False
    boolen_flag_second = False
    ## Barrier
    barrier_locations_list = []

    running = True
    num_of_player_clicks = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.mouse.get_pressed()[2]: # if player press mouse
                num_of_player_clicks = num_of_player_clicks + 1
                if num_of_player_clicks == 1:
                    temp_loc_start = pygame.mouse.get_pos() # (x,y) get location of mouse
                    start_col = temp_loc_start[0]//SQ_SIZE
                    start_row = temp_loc_start[1]//SQ_SIZE
                    start_location = (start_col, start_row)
                    print(start_location)
                    drawNode(screen, start_location)

                #if num_of_player_clicks == 2:
            elif pygame.mouse.get_pressed()[1]: # if player press mouse
                temp_loc_end = pygame.mouse.get_pos() # (x,y) get location of mouse
                end_col = temp_loc_end[0]//SQ_SIZE
                end_row = temp_loc_end[1]//SQ_SIZE
                end_location = (end_col, end_row)
                drawNode(screen, end_location)


            #elif num_of_player_clicks == 3:
            elif event.type == pygame.KEYDOWN: # if player press mouse
                if event.key == pygame.K_a:
                    print("jee")
                    path, open_list, closed_list = astar(start_location, end_location, board, barrier_locations_list)
                    reconstruct(screen,path)
                        #boolen_flag_first = True
                        #boolen_flag_second = True
                else:
                    continue

            elif pygame.mouse.get_pressed()[0]:
                temp_loc_barrier = pygame.mouse.get_pos() # (x,y) get location of mouse
                barrier_col = temp_loc_barrier[0]//SQ_SIZE
                barrier_row = temp_loc_barrier[1]//SQ_SIZE
                barrier_location = (barrier_col, barrier_row)
                barrier_locations_list.append(barrier_location)
                drawBarrier(screen, barrier_location)

        
        #if boolen_flag_first:
          #  boolen_flag_second = True
            #if i == len(closed_list) or ii == len(open_list): 
              #  boolen_flag_first = False
             #   boolen_flag_second = True
                #continue
            
            #drawOpenList(screen, open_list[ii].position)
            #drawClosedList(screen, closed_list[i].position)
          #  i = i + 1
          #  ii = ii + 1


        #if boolen_flag_second:
            #if j == len(path):
              #  boolen_flag_second == False
             #   continue
            #reconstruct(screen,path[j])
           # boolen_flag_second == False
            #j = j + 1


        redrawWindow(screen)
        pygame.display.flip()
        clock.tick(MAX_FPS)

def astar(start_position, end_position, board, barriers):

    print(barriers)
 ## Initialize both open and closed list
    open_list = []
    closed_list = []
    # additional list
    all_the_open_list_variables = []

    # Initialize start and end node
    start_node = Node(start_position, None)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0

    end_node = Node(end_position, None)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    # Add start node on the open list
    open_list.append(start_node)
    
    ## loop until open list is empty
    while len(open_list) > 0:

        ## let the current node equal to the node with the least f value
        current_node = open_list[0]
        current_index = 0

        for index, i in enumerate(open_list):
            if i.f < current_node.f:
                current_node = i
                current_index = index
        
        
        ## remove current node from the open list
        open_list.pop(current_index)
             
        ## add the currentNode to the closed list
        closed_list.append(current_node)

        ## if we have found the goal node
        if (current_node.position == end_node.position):
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            
            path = path[::-1]
            return path, all_the_open_list_variables, closed_list
        
        # directions where one can move
        directions = [(1,0), (0,1), (-1,0), (0,-1)]

        # allocate empty list for the node positions next to current nodes
        adjacent_nodes_positions = []
        
        # Generate these node positions that are next to the current node
        for i in directions:
            node_positions = (current_node.position[0]+i[0],current_node.position[1]+i[1])
            
            # if x or y value is out of the board
            if (node_positions[0] < 0 or node_positions[0] >= len(board) or node_positions[1] < 0 or node_positions[1] >= len(board)):
                continue

            # if threre is obstacle
            if (node_positions[0], node_positions[1]) in barriers:
                continue
            adjacent_nodes_positions.append(node_positions)

        
        
        # allocate empty list for the instance of nodes
        adjacent_nodes = []

        # make these new node instances and add them into list if they can be accsessed
        for i in range(len(adjacent_nodes_positions)):
            new_node = Node(adjacent_nodes_positions[i], current_node)
            adjacent_nodes.append(new_node)

        #print(adjacent_nodes[0].position)
    
        #'''
        for nod in adjacent_nodes:
            
            # Check if the adjacent node is in the closed list
            if len([closed_node for closed_node in closed_list if closed_node.position == nod.position]) > 0:
                continue
            
            # calculate h,g,f scores
            nod.g = current_node.g + math.sqrt((nod.position[0]+current_node.position[0])**2 + (nod.position[1]+current_node.position[1])**2) # Euclidian distance
            nod.h = abs(nod.position[0]+end_node.position[0]) + abs(nod.position[1]+end_node.position[1]) # Manhanttan distance
            nod.f = nod.g + nod.h 
            
            
            # Check if the nod already belong to the open list and if it belong check if its F score is now higher or lower
            if len([open_node for open_node in open_list if nod.position == open_node.position and nod.g > open_node.g]) > 0:
                continue

            # Add nod to the openlist
            open_list.append(nod)
            all_the_open_list_variables.append(nod)

def reconstruct(screen,path_variable):
    print(path_variable)
    for i,tuple in enumerate(path_variable):
        col_location = tuple[0]
        row_location = tuple[1]
        rect = pygame.Rect(col_location*SQ_SIZE, row_location*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        pygame.draw.rect(screen, pygame.Color("blue"), rect)
        clock = pygame.time.Clock()
        redrawWindow(screen)
        pygame.display.flip()
        clock.tick(10)
        

def drawClosedList(screen, closedListVariable):
    gap = WIDTH//DIMENSION
    col_location = closedListVariable[0]
    row_location = closedListVariable[1]
    rect = pygame.Rect(col_location*SQ_SIZE,row_location*SQ_SIZE,SQ_SIZE,SQ_SIZE)
    pygame.draw.rect(screen, pygame.Color("red"),rect) 

def drawOpenList(screen, openListVariable):
    col_location = openListVariable[0]
    row_location = openListVariable[1]
    rect = pygame.Rect(col_location*SQ_SIZE,row_location*SQ_SIZE,SQ_SIZE,SQ_SIZE)
    pygame.draw.rect(screen, pygame.Color("green"),rect) 


# make barrier
def drawBarrier(screen, location):
    gap = WIDTH//DIMENSION
    rect = pygame.Rect(location[0]*SQ_SIZE,location[1]*SQ_SIZE,SQ_SIZE,SQ_SIZE)
    pygame.draw.rect(screen, pygame.Color("orange"),rect)    

# Draws starting, ending and obstacle nodes
def drawNode(screen,location):
    
    gap = WIDTH//DIMENSION
    rect = pygame.Rect(location[0]*SQ_SIZE,location[1]*SQ_SIZE,SQ_SIZE,SQ_SIZE)
    pygame.draw.rect(screen, pygame.Color("white"),rect)
    
def drawGrid(screen):
    '''
    x = 0
    y = 0

    for i in range(DIMENSION):
        x = x + DIMENSION
        y = y + DIMENSION

        pygame.draw.line(screen,(255,255,255), (x, 0), (x, WIDTH))
        pygame.draw.line(screen,(255,255,255), (0, y), (WIDTH, y))

    '''
    for i in range(0,WIDTH,SQ_SIZE):
        #pygame.draw.line(screen, pygame.Color("black"),(0, i),(HEIGHT, 0))
        pygame.draw.line(screen, pygame.Color("black"),(i, 0),(i, WIDTH))
        for j in range(0,HEIGHT,SQ_SIZE):
            rect = pygame.Rect(i,j,SQ_SIZE,SQ_SIZE)
            pygame.draw.rect(screen, pygame.Color("white"),rect,1)

            
            
def redrawWindow(screen):
    drawGrid(screen)
    pygame.display.update()

if __name__ == "__main__": 
    main()