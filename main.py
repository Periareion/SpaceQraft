
#import pyglet
#from pyglet.gl import *

#config = Config(sample_buffers=1, samples=8)
#width, height = 600, 400
#window = pyglet.window.Window(width=width, height=height, config=config)
#fps_display = pyglet.window.FPSDisplay(window=window)
#pyglet.graphics.glEnable(pyglet.graphics.GL_DEPTH_TEST)

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from qraft import *

def rotate(square, qvector, angle):
    for q in square:
        q.rotate(qvector, angle)
        
def main(width, height, FPS=60):
    
    window = pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Qraft")
    
    t = 0
    dt = 1/FPS
    clock = pygame.time.Clock()
    
    gluPerspective(60, width/height, 0.1, 50.0)
    glTranslatef(0, 0, -2)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    light_vector = Q([0,0,-1])
    
    group = shapes.Group([
        shapes.Cuboid((0.5, 0, 0),(1, 0.5, 0.5),(0.85,0.3,0.25)),
        shapes.Cuboid((0.7, 0.25, 0),(0.3, 0.2, 0.4),(0.3,0.7,0.9))],
        position=Q([0.5,0,0]),
        unit_vectors=UNIT_QUATERNIONS.copy().rotate(Q([1,1,1]), math.tau/3))
    cubes = shapes.Group([group])#shapes.Cuboid(color=(0.3,0.3,0.7)), shapes.Cuboid((-0.5, 0, 0),(1, 0.5, 0.5),(0.5,0.2,0.2)), group])
    
    running = True
    while running:
        
        #gluLookAt
        
        key_presses = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    cubes.position.x += 0.1
                if event.key == pygame.K_s:
                    cubes.position.x -= 0.1
                if event.key == pygame.K_a:
                    cubes.position.y += 0.1
                if event.key == pygame.K_d:
                    cubes.position.y -= 0.1
                if event.key == pygame.K_q:
                    cubes.position.z += 0.1
                if event.key == pygame.K_e:
                    cubes.position.z -= 0.1
        
        glClearColor(0.2, 0.2, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        cubes.unit_vectors.rotate(Q([1,2,3]), 0.02)
        
        # Set the stage for drawing triangles
        glBegin(GL_TRIANGLES)
        cubes.render(light_vector=light_vector)
        glEnd()
        
        pygame.display.flip()
        
        t += dt
        clock.tick(FPS)
    
    pygame.quit()
    
if __name__ == "__main__":
    main(800, 600, 60)