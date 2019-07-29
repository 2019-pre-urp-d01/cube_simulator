
import logging
import sys
import math
logging.basicConfig(level=logging.INFO, \
        format='[%(asctime)s] %(message)s',\
        datefmt='%Y-%m-%d %H:%M:%S', \
        stream=sys.stdout)
        
import pygame
from pygame.locals import *

from cube import Cubes

class Config:
    def __init__(self):
        self.display_width = 800
        self.display_height = 600
        self.grid_size = 50

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
GRID_INIT_X = DISPLAY_WIDTH/2
GRID_INIT_Y = 200
GRID_SIZE = 30

def GetGridPosition(x,y,z):
    return (GRID_INIT_X+y*GRID_SIZE*math.sqrt(3)-x*GRID_SIZE*math.sqrt(3)
            ,GRID_INIT_Y+(x*GRID_SIZE+y*GRID_SIZE+z*GRID_SIZE*2)*0.9)


def DrawGridLine(d, loc, size, col=pygame.Color("black"), w=1):
    pygame.draw.line(d,col,
    GetGridPosition(loc[0], loc[1], loc[2]),
    GetGridPosition(loc[0]+size[0], loc[1]+size[1], loc[2]+size[2])
    ,w)

def DrawGridPlane(d, dir, loc, size, col, w=0):
    if dir == "z":
        pygame.draw.polygon(d, col,
        [GetGridPosition(loc[0]     ,loc[1]     ,loc[2]),
         GetGridPosition(loc[0]     ,loc[1]+size,loc[2]),
         GetGridPosition(loc[0]+size,loc[1]+size,loc[2]),
         GetGridPosition(loc[0]+size,loc[1]     ,loc[2])], w)
    if dir == "y":
        pygame.draw.polygon(d, col,
        [GetGridPosition(loc[0],loc[1]     ,loc[2]),
         GetGridPosition(loc[0],loc[1]+size,loc[2]),
         GetGridPosition(loc[0],loc[1]+size,loc[2]+size),
         GetGridPosition(loc[0],loc[1]     ,loc[2]+size)], w)
    if dir == "x":
        pygame.draw.polygon(d, col,
        [GetGridPosition(loc[0]     ,loc[1],loc[2]),
         GetGridPosition(loc[0]+size,loc[1],loc[2]),
         GetGridPosition(loc[0]+size,loc[1],loc[2]+size),
         GetGridPosition(loc[0]     ,loc[1],loc[2]+size)], w)


pygame.font.init()
FONT_CUBE = pygame.font.SysFont('Comic Sans MS',14)

def DrawGridCubePlane(d, direction, loc, val0="", val1="",col=None, val1Off = None):
    if col == None: # 0/1 mode
        if val0 == 0:
            DrawGridPlane(d, direction, loc,1,pygame.Color("grey20"))
        else:
            DrawGridPlane(d, direction, loc,1,pygame.Color("white"))
    else:
        DrawGridPlane(d, direction, loc,1,pygame.Color("red"))

    DrawGridPlane(d, direction, loc,1,pygame.Color("black"), 2)
    if direction == "z":
        off = (0.1, 0.1, 0.1)
        if val1Off == None:
            val1Off = (0.3, -0.3, 0.2)
    elif direction == "y":
        off = (-0.1, 0.3, 0.4)
        if val1Off == None:
            val1Off = (0.0, -0.3, 0.4)
    elif direction == "x":
        off = (0.6, 0.0, 0.2)
        if val1Off == None:
            val1Off = (0.3, -0.0, 0.2)
    d.blit(FONT_CUBE.render(str(val0),False, (0,0,0)),GetGridPosition(loc[0]+off[0],loc[1]+off[1],loc[2]+off[2]))
    d.blit(FONT_CUBE.render(str(val1),False, (0,0,0)),GetGridPosition(loc[0]+off[0]+val1Off[0],loc[1]+off[1]+val1Off[1],loc[2]+off[2]+val1Off[2]))

def DrawCubes(d, cubes):
    # U
    plane_char =    ['U', 'F', 'R', 'L', 'B', 'D']
    cols =          [pygame.Color("red"), pygame.Color("Green"), pygame.Color("white"), pygame.Color("yellow"), pygame.Color("pink"), pygame.Color("Blue")]
    data_location = [(1,1,0), (3,1,1), (1,3,1), (1,-4,1), (-4,1,1), (8,8,0)]
    direction =     [ "z", "y", "x", "x", "y", "z"]
    bit_location = [
        [(0,2,0), (1,2,0), (2,2,0), (2,1,0), (2,0,0), (1,0,0), (0,0,0), (0,1,0)],
        [(3,2,0), (3,2,1), (3,2,2), (3,1,2), (3,0,2), (3,0,1), (3,0,0), (3,1,0)],
        [(0,3,0), (0,3,1), (0,3,2), (1,3,2), (2,3,2), (2,3,1), (2,3,0), (1,3,0)],
        [(2,-4,0), (2,-4,1), (2,-4,2), (1,-4,2), (0,-4,2), (0,-4,1), (0,-4,0), (1,-4,0)],
        [(-4,2,0), (-4,2,1), (-4,2,2), (-4,1,2), (-4,0,2), (-4,0,1), (-4,0,0), (-4,1,0)],
        [(9,9,0), (8,9,0), (7,9,0), (7,8,0), (7,7,0), (8,7,0), (9,7,0), (9,8,0)]
    ]
    # Z line
    DrawGridLine(d, (3,0,3),(0,0,4),pygame.Color("grey53"),w=3)
    DrawGridLine(d, (0,3,3),(0,0,4),pygame.Color("grey53"),w=3)

    # X line        
    DrawGridLine(d, (0,0,0),(-4,0,0),pygame.Color("grey53"),w=3)
    DrawGridLine(d, (0,3,3),(-4,0,0),pygame.Color("grey53"),w=3)
    # Y line
    DrawGridLine(d, (0,0,0),(0,-4,0),pygame.Color("grey53"),w=3)
    DrawGridLine(d, (3,0,3),(0,-4,0),pygame.Color("grey53"),w=3)

    for pIndex in range(6):
        for cIndex in range(8):
            DrawGridCubePlane(d, direction[pIndex], bit_location[pIndex][cIndex], val0=cubes.cube.cell_bit[pIndex][cIndex], val1="#%d"%cIndex,val1Off = (0.1, -0.1, 0.3))
        DrawGridCubePlane(d, direction[pIndex], data_location[pIndex], val0=cubes.cube.cell_data[pIndex], val1=plane_char[pIndex]+"/"+cubes.cube.cell_func[pIndex], col=cols[pIndex])

def DrawUI(d):
    
    pass

if __name__ == "__main__":
    pygame.init()
    c = Config()
    cubes = Cubes()
    main_display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption('CUBE GUI Compiler')
    clock = pygame.time.Clock()
    while True:
        evt={"QUIT": False,
        "LEFT": False, "RIGHT": False, "UP": False, "DOWN": False}
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT: evt["QUIT"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: evt["LEFT"] = True
                if event.key == pygame.K_RIGHT: evt["RIGHT"] = True

        if evt["QUIT"]:
            pygame.quit()
            break
        # Fill with white
        main_display.fill((255,255,255))
        
        # Draw cube!
        DrawCubes(main_display, cubes)
        # Draw UI!
        DrawUI(main_display)
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()