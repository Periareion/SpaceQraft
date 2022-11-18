
from aquaternion import *

from . import utils

class Entity:
    
    def __init__(self,
        position: Quaternion = None,
        unit_vectors: UnitVectors = None,
    ):
        self.position = utils.default(Q([0,0,0]), position)
        self.unit_vectors = utils.default(UV.copy(), unit_vectors)

    def inherit(self, parent_position: Quaternion, parent_unit_vectors: UnitVectors):
        self.true_position = parent_position + self.position.morphed(*parent_unit_vectors)
        self.true_unit_vectors = self.unit_vectors.morphed(*parent_unit_vectors)
        
    def absolute_translation(self, offset: Quaternion):
        self.position += offset
        
    def relative_translation(self, offset: Quaternion):
        self.position += offset.morphed(*self.unit_vectors)