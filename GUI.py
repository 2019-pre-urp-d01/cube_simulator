import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from cube import Cube


DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

INPUT_RAW = {"UP":0, "LEFT":0, "DOWN":0, "RIGHT":0, "SCRLUP":0, "SCRLDN":0}

def Render3d():
    global DISPLAY_WIDTH, DISPLAY_HEIGHT

    ### clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    ### projection mode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, DISPLAY_WIDTH/DISPLAY_HEIGHT, 0.1, 50.0)

    if input_rotateY != 0:
        glRotatef(1, 0, input_rotateY*3, 0)
    if input_rotateX != 0:
        glRotatef(1, input_rotateX*3, 0, 0)
#                    glScalef(1*input_scale,1*input_scale,1*input_scale)
        
    # glRotatef(25, 2, 1, 0)
    glTranslatef(0,0, -10)
    ### modelview mode
    glMatrixMode(GL_MODELVIEW)

    ### setup 3d shader
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

#--- 2D projection function
def Render2d():
    global DISPLAY_WIDTH, DISPLAY_HEIGHT

    ### projection mode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, DISPLAY_WIDTH, DISPLAY_HEIGHT, 0.0)

    ### modelview mode
    glMatrixMode(GL_MODELVIEW)

    ### setup 2d shader
    glDisable(GL_DEPTH_TEST)

def reshape(new_width, new_height):
    global DISPLAY_WIDTH, DISPLAY_HEIGHT
    ### apply new window size
    width = new_width
    height = new_height

# hud
def Hud():
    ### draw Hud
    glBegin(GL_RECTANGLES)
    
    glColor3f(1.0, 1.0, 1.0)
    gap = 10
    grid = 100
    glVertex2f(gap,      gap)
    glVertex2f(grid-gap, gap)
    glVertex2f(grid-gap, grid-gap)
    glVertex2f(gap,      grid-gap)
    
    glEnd() 

def Draw():
    glPushMatrix()
    Render3d()
    # Cube()
    glPopMatrix()

    glPushMatrix()
    Render2d()
    Hud()
    glPopMatrix()
    
def GetInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:   INPUT_RAW["LEFT"]  = 1
            if event.key == pygame.K_RIGHT:  INPUT_RAW["RIGHT"] = 1
            if event.key == pygame.K_UP:     INPUT_RAW["UP"]    = 1
            if event.key == pygame.K_DOWN:   INPUT_RAW["DOWN"]  = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:   INPUT_RAW["LEFT"]  = 0
            if event.key == pygame.K_RIGHT:  INPUT_RAW["RIGHT"] = 0
            if event.key == pygame.K_UP:     INPUT_RAW["UP"]    = 0
            if event.key == pygame.K_DOWN:   INPUT_RAW["DOWN"]  = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:            INPUT_RAW["SCRLUP"] = 1
            if event.button == 5:            INPUT_RAW["SCRLDN"] = 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:            INPUT_RAW["SCRLUP"] = 0
            if event.button == 5:            INPUT_RAW["SCRLDN"] = 0
    
# Main initialize
if __name__ == "__main__":
    # Initializing screen
    pygame.init()
    screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT], DOUBLEBUF|OPENGL)
    
    while True:
        GetInput()                    # Get Input
        Draw()                        # Draw!
        pygame.display.flip()         # Pygame delay
        pygame.time.wait(10)