
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

DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800
GRID_INIT_X = DISPLAY_WIDTH/2
GRID_INIT_Y = 200
GRID_SIZE = 33

pygame.font.init()
FONT_CUBE = pygame.font.Font('d2coding.ttc',18)
FONT_COMMAND = pygame.font.Font('d2coding.ttc',40)
FONT_CONSOLE = pygame.font.Font('d2coding.ttc',30)

UI_LEFT_X = 0
UI_LEFT_Y = 500
UI_RIGHT_X = 770
UI_RIGHT_Y = 500
UI_GAP = 5
UI_SIZE = 60

BUTTONS_LEFT = [
    ['U', 'F', 'R', 'L', 'B', 'D'],
    ["U'", "F'", "R'", "L'", "B'", "D'"],
    ['u', 'f', 'r', 'l', 'b', 'd'],
    ["u'", "f'", "r'", "l'", "b'", "d'"],
    ['M', 'S', 'E', "M'", "S'", "E'"]
]
BUTTONS_RIGHT = [
    ["I", "P", "X", "*", "=", "C"],
    ["(", ")", "!", "-", "+", "m", "p"],
    ["[", "]", "{", "}"]
]

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



def DrawGridCubePlane(d, direction, loc, val0="", val1="",col=None, val1Off = None):
    if col == None: # 0/1 mode
        if val0 == 0:
            DrawGridPlane(d, direction, loc,1,pygame.Color("grey20"))
        else:
            DrawGridPlane(d, direction, loc,1,pygame.Color("white"))
    else:
        DrawGridPlane(d, direction, loc,1,col)

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
    # Input, Output, Inout, And, Nand, Or, Nor, Xor, Xnor, Not, One, Shift
    cols =          {"Input":pygame.Color("grey50"), "Output":pygame.Color("grey90"), "Inout":pygame.Color("white"),
                    "And": pygame.Color("yellow"), "Nand":pygame.Color("orange"),
                    "Or": pygame.Color("Blue"), "Nor":pygame.Color("aquamarine"),
                    "Xor": pygame.Color("Red"), "Xnor":pygame.Color("pink"),
                    "Not": pygame.Color("Green"),"One":pygame.Color("purple"),
                    "Shift": pygame.Color("ivory")}
    data_location = [(1,1,0), (3,1,1), (1,3,1), (1,-4,1), (-4,1,1), (8,8,0)]
    direction =     [ "z", "y", "x", "x", "y", "z"]
    bit_location = [
        [(0,2,0), (1,2,0), (2,2,0), (2,1,0), (2,0,0), (1,0,0), (0,0,0), (0,1,0)],
        [(3,2,0), (3,2,1), (3,2,2), (3,1,2), (3,0,2), (3,0,1), (3,0,0), (3,1,0)],
        [(0,3,0), (0,3,1), (0,3,2), (1,3,2), (2,3,2), (2,3,1), (2,3,0), (1,3,0)],
        [(2,-4,0), (2,-4,1), (2,-4,2), (1,-4,2), (0,-4,2), (0,-4,1), (0,-4,0), (1,-4,0)],
        [(-4,0,0), (-4,0,1), (-4,0,2), (-4,1,2), (-4,2,2), (-4,2,1), (-4,2,0), (-4,1,0)],
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
        DrawGridCubePlane(d, direction[pIndex], data_location[pIndex], val0=cubes.cube.cell_data[pIndex], val1=plane_char[pIndex]+"/"+cubes.cube.cell_func[pIndex], col=cols[cubes.cube.cell_func[pIndex]])

    # Core Cell
    d.blit(FONT_CONSOLE.render("CORE:%d"%cubes.cube.cell_core,False, (0,0,0)),GetGridPosition(8,-1,0))

def DrawUI(d, buttons, UI_X, UI_Y, UI_GAP, UI_SIZE):
    for yind,lst in enumerate(buttons):
        for xind, val in enumerate(lst):
            row = xind; col = yind
            pygame.draw.polygon(d, pygame.Color("black"),
            [(UI_X+UI_SIZE*(row)+UI_GAP  ,UI_Y+UI_SIZE*(col)+UI_GAP),
            (UI_X+UI_SIZE*(row+1)-UI_GAP,UI_Y+UI_SIZE*(col)+UI_GAP),
            (UI_X+UI_SIZE*(row+1)-UI_GAP,UI_Y+UI_SIZE*(col+1)-UI_GAP),
            (UI_X+UI_SIZE*(row)+UI_GAP  ,UI_Y+UI_SIZE*(col+1)-UI_GAP)], 3)
            d.blit(FONT_COMMAND.render(val,False, (0,0,0)),(UI_X+UI_SIZE*(row+0.2)+UI_GAP  ,UI_Y+UI_SIZE*(col+0.1)+UI_GAP))

def GetCommand(pos):
    # print(pos)
    if pos[0]<UI_LEFT_X and pos[1]<UI_LEFT_Y and pos[0]<UI_RIGHT_X and pos[1]<UI_RIGHT_Y:
        return ""
    
    # Check if it's left
    if pos[0]<DISPLAY_WIDTH/2:
        x = pos[0]-UI_LEFT_X
        y = pos[1]-UI_LEFT_Y
    else:
        x = pos[0]-UI_RIGHT_X
        y = pos[1]-UI_RIGHT_Y

    if x%UI_SIZE<UI_GAP or x%UI_SIZE>UI_SIZE-UI_GAP:
        return ""
    if y%UI_SIZE<UI_GAP or y%UI_SIZE>UI_SIZE-UI_GAP:
        return ""
    
    xind = x//UI_SIZE
    yind = y//UI_SIZE

    res = ""
    try:
        if pos[0]<DISPLAY_WIDTH/2:
            res = BUTTONS_LEFT[yind][xind]
        else:
            res = BUTTONS_RIGHT[yind][xind]
    except:
        print("Minor problem...")

    return res

if __name__ == "__main__":
    pygame.init()
    cubes = Cubes()
    main_display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption('CUBE GUI Compiler')
    clock = pygame.time.Clock()
    input_value = ""
    output_value = ""
    while True:
        command = ""
        evt={"QUIT": False,
        "LEFT": False, "RIGHT": False, "UP": False, "DOWN": False}
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT: evt["QUIT"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: evt["LEFT"] = True
                if event.key == pygame.K_RIGHT: evt["RIGHT"] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                command = GetCommand(pygame.mouse.get_pos())
            # Text handing
            if event.type == pygame.KEYDOWN:
                input_value = event.unicode
        if evt["QUIT"]:
            pygame.quit()
            break
        

        # Fill with white
        main_display.fill((255,255,255))
        if input_value!="":
            main_display.blit(FONT_CONSOLE.render("Input:%s(%d)"%(input_value,ord(input_value[0])),False, (0,0,0)),(UI_RIGHT_X+UI_GAP  ,UI_RIGHT_Y-0.7*UI_SIZE+UI_GAP))
        else:
            main_display.blit(FONT_CONSOLE.render("Input:",False, (0,0,0)),(UI_RIGHT_X+UI_GAP  ,UI_RIGHT_Y-0.7*UI_SIZE+UI_GAP))
        if output_value!="":
            main_display.blit(FONT_CONSOLE.render("Output:%s(%d)"%(output_value,ord(output_value[0])),False, (0,0,0)),(UI_RIGHT_X+UI_GAP+UI_SIZE*3  ,UI_RIGHT_Y-0.7*UI_SIZE+UI_GAP))
        else:
            main_display.blit(FONT_CONSOLE.render("Output:",False, (0,0,0)),(UI_RIGHT_X+UI_GAP+UI_SIZE*3  ,UI_RIGHT_Y-0.7*UI_SIZE+UI_GAP))
            
        # command
        if command != "":
            logging.info("Executing %s"%command)
            if command == "I":
                cubes.Execute(command, input_value)
                input_value = ""
            else:
                output_value = cubes.Execute(command)


        # Draw cube!
        DrawCubes(main_display, cubes)
        # Draw UI!
        DrawUI(main_display, BUTTONS_LEFT, UI_LEFT_X, UI_LEFT_Y, UI_GAP, UI_SIZE)
        DrawUI(main_display, BUTTONS_RIGHT, UI_RIGHT_X, UI_RIGHT_Y, UI_GAP, UI_SIZE)


        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()