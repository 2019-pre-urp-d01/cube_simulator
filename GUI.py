import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
   #--- 3D projection function

width = 800
height = 600
def render3d():

    global width, height

    ### clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, width, height)

    ### projection mode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 50.0)

    # glRotatef(25, 2, 1, 0)
    glTranslatef(0,0, -10)
    ### modelview mode
    glMatrixMode(GL_MODELVIEW)

    ### setup 3d shader
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

#--- 2D projection function
def render2d():

    global width, height

    ### projection mode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, width, height, 0.0)

    ### modelview mode
    glMatrixMode(GL_MODELVIEW)

    ### setup 2d shader
    glDisable(GL_DEPTH_TEST)

#--- reshape function
def reshape(new_width, new_height):

    global width, height

    ### apply new window size
    width = new_width
    height = new_height

#--- 2D triangle function
def scene2d():

    ### draw triangle
    glBegin(GL_TRIANGLES)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0, 0)
    glVertex2f(100, 0)
    glVertex2f(0, 100)

    glEnd() 

def draw():
    glPushMatrix()
    render3d()
    Cube()
    glPopMatrix()

    glPushMatrix()
    render2d()
    scene2d()
    glPopMatrix()

#--- only run if this is the main module
if __name__ == "__main__":
    pygame.init()

    display = [800,600]
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    white = (255,0,0)
    
    input_rotateX = 0
    input_rotateY = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    input_rotateY = 1
                if event.key == pygame.K_RIGHT:
                    input_rotateY = -1

                if event.key == pygame.K_UP:
                    input_rotateX = -1
                if event.key == pygame.K_DOWN:
                    input_rotateX = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    input_rotateY = 0
                
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    input_rotateX = 0
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    input_scale = 1.1
                    glScalef(1*input_scale,1*input_scale,1*input_scale)
                if event.button == 5:
                    input_scale = 0.9
                    glScalef(1*input_scale,1*input_scale,1*input_scale)

        if input_rotateY != 0:
            glRotatef(1, 0, input_rotateY*3, 0)
        if input_rotateX != 0:
            glRotatef(1, input_rotateX*3, 0, 0)

        draw()
        pygame.display.flip()
        pygame.time.wait(10)
