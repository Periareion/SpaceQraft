
from aquaternion import *

class Autopilot:

    def __init__(self, craft):
        self.craft = craft
        self.target_direction = None
        self.target = None

    def update(self):
        if self.target_direction is not None:
            anomaly = self.target_direction.unmorphed(*self.craft.unit_vectors)