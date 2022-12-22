
import math

import pygame

from aquaternion import *

from .entity import Entity

class Camera(Entity):
    
    def __init__(self,
        position: Quaternion,
        unit_vectors: UnitVectors,
        field_of_view: float,
    ):
        super().__init__(position, unit_vectors)
        self.field_of_view = field_of_view
    
    @property
    def focal_length(self):
        """Returns the focal length, with a window width of 2."""
        return 2 / (2 * math.tan(math.radians(self.field_of_view / 2)))


    def rotate(self, axis, angle):
        self.unit_vectors.rotate(axis, angle)


    def movement(self, mouse, keyboard):
        self.rotate(self.unit_vectors[1], mouse.delta_position[0]/600)
        self.rotate(self.unit_vectors[0], -mouse.delta_position[1]/600)
        
        if keyboard.state[pygame.K_q]: self.unit_vectors.rotate(self.unit_vectors[2], -0.05)
        if keyboard.state[pygame.K_e]: self.unit_vectors.rotate(self.unit_vectors[2], 0.05)
        
        if keyboard.state[pygame.K_w]: self.relative_translation(Q([0, 0, 1])*0.05)
        if keyboard.state[pygame.K_s]: self.relative_translation(Q([0, 0, -1])*0.05)
        if keyboard.state[pygame.K_a]: self.relative_translation(Q([-1, 0, 0])*0.05)
        if keyboard.state[pygame.K_d]: self.relative_translation(Q([1, 0, 0])*0.05)
        if keyboard.state[pygame.K_SPACE]: self.relative_translation(Q([0, -1, 0])*0.05)
        if keyboard.state[pygame.K_LSHIFT]: self.relative_translation(Q([0, 1, 0])*0.05)
