
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

from OpenGL.GL import glClearDepth, glDepthFunc, glEnable, glClearColor, glClear, glBegin, glEnd, glMatrixMode, glLoadIdentity, glColor3fv, glVertex3fv
from OpenGL.GL import GL_LESS, GL_DEPTH_TEST, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRIANGLES, GL_LINES, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective

import aquaternion as aq

class Scene:

    def __init__(self, name, width, height, background_color=(0.2, 0.2, 0.3, 1.0), FPS=60):
        self.name = name
        self.width = width
        self.height = height
        self.background_color = background_color

        self.window = pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(pygame.image.load('qraft/assets/icon.png'))

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        self.objects = []
        self.lines = []

    def update(self):
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    
    def render(self, camera, light_vector):
        relative_light_vector = light_vector.unmorphed(*camera.unit_vectors)

        glBegin(GL_TRIANGLES)
        for obj in self.objects:
            obj.render(
                (obj.position - camera.position).unmorphed(*camera.unit_vectors),# - obj.position.morphed(*camera.unit_vectors),
                aq.UNIT_QUATERNIONS.unmorphed(*camera.unit_vectors),
                relative_light_vector)
        glEnd()

        for line in self.lines:
            relative_vertices = (line[0] + (-camera.position)).unmorphed(*camera.unit_vectors)
            #relative_vertices.unmorphed(*camera.unit_vectors)
            #relative_vertices = [(vertex - camera.position) for vertex in line[0]]
            glBegin(GL_LINES)
            glColor3fv(line[1])
            n = len(relative_vertices)
            for i in range(n-1):
                glVertex3fv(relative_vertices[i].vector3)
                glVertex3fv(relative_vertices[i+1].vector3)
            glEnd()

    def set_FOV(self, FOV):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, self.width/self.height, 0.1, 200.0)
        glMatrixMode(GL_MODELVIEW)


class Camera:

    def __init__(self, position, unit_vectors, field_of_view):
        self.position = position
        self.velocity = aq.Q([0,0,0])
        self.unit_vectors = unit_vectors
        self.field_of_view = field_of_view
    
    def translate_rel(self, offset):
        self.position += offset.morphed(*self.unit_vectors)*self.position.norm**0.7

    def translate_abs(self, offset):
        self.position += offset
    
    def rotate(self, axis, angle):
        self.unit_vectors.rotate(axis, angle)

    def update(self, mouse, keyboard):
        self.rotate(self.unit_vectors[1], -mouse.delta_position[0]/600)
        self.rotate(self.unit_vectors[0], -mouse.delta_position[1]/600)
        
        if keyboard.state[pygame.K_q]: self.unit_vectors.rotate(self.unit_vectors[2], 0.05)
        if keyboard.state[pygame.K_e]: self.unit_vectors.rotate(self.unit_vectors[2], -0.05)
        
        if keyboard.state[pygame.K_w]: self.translate_rel(aq.Q([0, 0, -1])*0.03)
        if keyboard.state[pygame.K_s]: self.translate_rel(aq.Q([0, 0, 1])*0.03)
        if keyboard.state[pygame.K_a]: self.translate_rel(aq.Q([-1, 0, 0])*0.03)
        if keyboard.state[pygame.K_d]: self.translate_rel(aq.Q([1, 0, 0])*0.03)
        if keyboard.state[pygame.K_SPACE]: self.translate_rel(aq.Q([0, 1, 0])*0.03)
        if keyboard.state[pygame.K_LSHIFT]: self.translate_rel(aq.Q([0, -1, 0])*0.03)

        self.position += self.velocity / 60


class Mouse:
    
    def __init__(self, width=600, height=400):
        self.half_width, self.half_height = width // 2, height // 2

        self.pressed = pygame.mouse.get_pressed(5)
        
        self.toggle_focus = False
        self.focused = False
        self.position = None
        self.delta_position = (0, 0)
        self.update()
    
    def update(self):
        
        new_pressed = pygame.mouse.get_pressed(5)
        self.downclicks = tuple((not self.pressed[i] and new_pressed[i] for i in range(5)))
        self.upclicks = tuple((self.pressed[i] and not new_pressed[i] for i in range(5)))
        self.pressed = new_pressed

        if pygame.mouse.get_focused():
            if self.downclicks[1]: self.toggle_focus = True
                
            if self.toggle_focus:
                self.focused = not self.focused
                if self.focused: self.hide()
                else:            self.show()

                self.toggle_focus = False
                self.position = self.half_width, self.half_height
                pygame.mouse.set_pos(self.position)

            if self.focused:
                new_position = pygame.mouse.get_pos()
                self.delta_position = new_position[0]-self.position[0], new_position[1]-self.position[1]
                pygame.mouse.set_pos(self.position)

            else:
                if self.position is None:
                    self.position = pygame.mouse.get_pos()
                new_position = pygame.mouse.get_pos()
                self.delta_position = new_position[0]-self.position[0], new_position[1]-self.position[1]
                self.position = new_position
        else:
            self.position = None

    def hide(self):
        pygame.mouse.set_visible(False)

    def show(self):
        pygame.mouse.set_visible(True)


class Keyboard:

    def __init__(self):
        self.state = pygame.key.get_pressed()
    
    def update(self):
        new_state = pygame.key.get_pressed()
        self.downs = pygame.key.ScancodeWrapper((now and not then for (now, then) in zip(new_state, self.state)))
        self.ups = pygame.key.ScancodeWrapper((not now and then for (now, then) in zip(new_state, self.state)))
        self.state = new_state
