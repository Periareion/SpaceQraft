
from aquaternion import *

from autopilot import Autopilot
from geometry import Mesh, Group

control_actions = {
    'pitch+': False,
    'pitch-': False,
    'yaw+': False,
    'yaw-': False,
    'roll+': False,
    'roll-': False,
    'x+': False,
    'x-': False,
    'y+': False,
    'y-': False,
    'z+': False,
    'z-': False,
}

class Craft:

    def __init__(self):

        self.position = Q([0, 0, 0])
        self.velocity = Q([0, 0, 0])

        self.unit_vectors = UV.copy()
        self.axis_of_rotation = Q([0, 0, 0])

        if not hasattr(self, 'parts'):
            self.parts = []
        
        self.mass, self.center_of_mass = Craft.get_mass(self.parts)

        self.control_actions = control_actions.copy()
        self.autopilot = Autopilot(self)
    
    @staticmethod
    def get_mass(parts):
        mass = sum([part.mass for part in parts])
        center_of_mass = sum([part.center_of_mass*part.mass for part in parts])/mass
        return mass, center_of_mass
    
    def update(self, dt=1/60, key_presses=None):

        self.position += self.velocity * dt
        self.unit_vectors.rotate(self.axis_of_rotation, self.axis_of_rotation.norm)