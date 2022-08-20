
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
        
def main(width, height, FPS=60):
    
    window = pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Qraft')
    pygame.display.set_icon(pygame.image.load('qraft/assets/icon.png'))
    
    t = 0
    dt = 1/FPS
    clock = pygame.time.Clock()
    
    gluPerspective(60, width/height, 0.1, 50.0)
    glTranslatef(0, 0, -3)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    light_vector = Q([1,-1.5,-2])
    
    from copy import copy
    
    # Make video with Pixies' song "Allison".
    amogus = gm.Group([gm.Group([
        gm.Cuboid((0.65, 0, 0),(0.65, 0.5, 0.55),(0.85,0.3,0.25)),
        gm.Cuboid((0.5, -0.3, 0),(0.5, 0.2, 0.4),(0.85,0.3,0.25)),
        gm.Cuboid((0.3, 0, 0.15),(0.5, 0.4, 0.25),(0.85,0.3,0.25)),
        gm.Cuboid((0.3, 0, -0.15),(0.5, 0.4, 0.25),(0.85,0.3,0.25)),
        gm.Cuboid((0.7, 0.25, 0),(0.3, 0.2, 0.4),(0.3,0.7,0.9)),
        gm.Cuboid((0.8, 0.25, -0.1),(0.05, 0.21, 0.1),(0.8,0.9,1))],
        position=[-0.5,0,0])])
    
    amogi = gm.Group([
        gm.Group([(amogus)], [0,0,1]),
        gm.Group([(amogus)], [0,0,-1])])
    
    cubes = gm.Group([
        gm.Cuboid(color=(0.3,0.3,0.7)),
        gm.Cuboid((-0.5, 0, 0),(1, 0.5, 0.5),(0.5,0.2,0.2)),
        gm.Cuboid((1, 0, 0),(0.65, 0.5, 0.55),(0.35,0.9,0.25))])

    sphere = gm.Group([gm.Sphere(radius=1)])
    k = 0
    running = True
    while running:
        
        # TODO: add functionality utilizing gluLookAt
        
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
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            sphere.unit_vectors.rotate(Q([1,0,0]), 0.05)
        if keys[pygame.K_w]:
            sphere.unit_vectors.rotate(Q([-1,0,0]), 0.05)
        if keys[pygame.K_e]:
            sphere.unit_vectors.rotate(Q([0,0,1]), 0.05)
        if keys[pygame.K_q]:
            sphere.unit_vectors.rotate(Q([0,0,-1]), 0.05)
        if keys[pygame.K_a]:
            sphere.unit_vectors.rotate(Q([0,1,0]), 0.05)
        if keys[pygame.K_d]:
            sphere.unit_vectors.rotate(Q([0,-1,0]), 0.05)
        
        glClearColor(0.2, 0.2, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # Set the stage for drawing triangles
        glBegin(GL_TRIANGLES)
        #amogi.render(light_vector=light_vector)
        sphere.render(light_vector=light_vector)
        glEnd()
        
        pygame.display.flip()
        
        t += dt
        clock.tick(FPS)
        fps = clock.get_fps()
        if not (k:=k+1)%30:print(fps)

    
    pygame.quit()
    
if __name__ == "__main__":
    main(800, 600, 60)