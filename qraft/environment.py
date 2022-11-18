
import pygame

import aquaternion as aq


class Scene:

    def __init__(self, name, width, height, background_color=(0.2, 0.2, 0.3, 1.0), FPS=60):
        self.name = name
        self.width = width
        self.height = height
        self.background_color = background_color

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(pygame.image.load('qraft/assets/icon.png'))

        self.objects = []
        self.lines = []


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
