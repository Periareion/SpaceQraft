
from geometry import Group

class Part(Group):

    def __init__(self, shapes=None, position=None, unit_vectors=None, density=1000):
        super().__init__(shapes, position, unit_vectors)
        self.density = density
        self.mass = self.density * self.volume
        self.center_of_mass = sum([shape.position*shape.volume for shape in self.shapes])/self.volume