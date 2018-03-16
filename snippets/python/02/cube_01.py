# https://stackoverflow.com/questions/30745703/rotating-a-cube-using-quaternions-in-pyopengl



import numpy
from math import *
from quat import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

axis_points = (
    (-6.0, 0.0, 0.0),
    ( 6.0, 0.0, 0.0),
    ( 0.0,-6.0, 0.0),
    ( 0.0, 6.0, 0.0),
    ( 0.0, 0.0,-6.0),
    ( 0.0, 0.0, 6.0)
    )

axes = (
    (0,1),
    (2,3),
    (4,5)
    )


verticies = (
    (-3.0,-3.0, 3.0),
    (-3.0, 3.0, 3.0),
    ( 3.0, 3.0, 3.0),
    ( 3.0,-3.0, 3.0),
    (-3.0,-3.0,-3.0),
    (-3.0, 3.0,-3.0),
    ( 3.0, 3.0,-3.0),
    ( 3.0,-3.0,-3.0),
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,3),
    (7,4),
    (7,6)
    )

surfaces = (
    (0,1,2,3),
    (3,2,6,7),
    (7,6,5,4),
    (4,5,1,0),
    (1,5,6,2),
    (4,0,3,7),
    )

colors = (
    (0.769,0.118,0.227), # Red
    (  0.0,0.318,0.729), # Blue
    (  1.0,0.345,  0.0), # Orange
    (  0.0, 0.62,0.376), # Green
    (  1.0,  1.0,  1.0), # White
    (  1.0,0.835,  0.0), # Yellow
    )


def Axis():
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    for axis in axes:
        for point in axis:
            glVertex3fv(axis_points[point])
    glEnd()

def Cube():
    glBegin(GL_QUADS)
    for color,surface in zip(colors,surfaces):
        glColor3fv(color)
        for vertex in surface:
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0,0,0))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (1800,1600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # Using depth test to make sure closer colors are shown over further ones
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Default view
    gluPerspective(45, (display[0]/display[1]), 0.05, 50.0)
    glTranslatef(0.0,0.0,-25)


    inc_x = 0
    inc_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                print "Modelview Matrix:"
                print glGetFloatv(GL_MODELVIEW_MATRIX)

                #Rotating about the x axis
                if event.key == pygame.K_UP:
                    inc_x =  pi/100
                if event.key == pygame.K_DOWN:
                    inc_x = -pi/100

                # Rotating about the y axis
                if event.key == pygame.K_LEFT:
                    inc_y =  pi/100
                if event.key == pygame.K_RIGHT:
                    inc_y = -pi/100

                # Reset to default view
                if event.key == pygame.K_SPACE:
                    glLoadIdentity()
                    gluPerspective(45, (display[0]/display[1]), 0.05, 50.0)
                    glTranslatef(0.0,0.0,-25)

            if event.type == pygame.KEYUP:
                # Stoping rotation
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    inc_x = 0.0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    inc_y = 0.0

        rot_x = normalize(axisangle_to_q((1.0,0.0,0.0), inc_x))
        rot_y = normalize(axisangle_to_q((0.0,1.0,0.0), inc_y))

        tot_rot = q_to_mat4(q_mult(rot_x,rot_y))
        glMultMatrixf(tot_rot)


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        Axis()
        pygame.display.flip()
        pygame.time.wait(10)

main()
