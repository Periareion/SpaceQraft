
try:
    from .aquaternion import *
    from .utils import validate_types
    from . import graphics
except ImportError:
    from aquaternion import *
    from utils import validate_types
    import graphics

class Polygon:
    
    def initialize(self, vertices, n):
        Polygon.check_vertices(vertices, n)
        self.vertices = vertices
    
    @classmethod
    def check_vertices(cls, vertices, n):
        if len(vertices) != n:
            raise IndexError(f"Polygon must have {n} vertices. ({vertices})")
        if not validate_types(vertices, Quaternion):
            raise TypeError("Vertices must be Quaternion instances.")


class Triangle(Polygon):
    n = 3
    
    def __init__(self, vertices):
        super().initialize(vertices, self.n)


class Tetragon(Polygon):
    n = 4
    
    def __init__(self, vertices):
        super().initialize(vertices, self.n)


class Mesh:
    
    def __init__(self, position):
        self.position = Q(position)

    def render(self, position=Q([0,0,0]), unit_vectors=UNIT_QUATERNIONS.copy(), light_vector=Q([0,0,0])):
        for face in self.faces:
            qvertices = QA([(vertex + self.position).morph(*unit_vectors) for vertex in self.qvertices])
            graphics.draw_tetragon(
                [(qvertices[vertex] + position) for vertex in face],
                self.color,
                light_vector)


class Cuboid(Mesh):

    vertices = ((-1, -1, -1), (-1, -1, 1),
                (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1),
                (1, 1, -1), (1, 1, 1))

    edges = ((0, 4), (1, 5), (2, 6), (3, 7),
             (0, 2), (1, 3), (4, 6), (5, 7),
             (0, 1), (2, 3), (4, 5), (6, 7))

    faces = ((0, 1, 3, 2), (0, 4, 5, 1), (0, 4, 6, 2),
             (7, 5, 4, 6), (7, 6, 2, 3), (7, 3, 1, 5))

    def __init__(self,
                 position=(0,0,0),
                 size=(1,1,1),
                 color=(1,1,1)):
        super().__init__(position)
        
        self.size = size
        self.color = color
        self.volume = math.prod(size)
        
        self.qvertices = QuaternionArray(
            [0.5*Q(vertex).morph(self.size[0]*qi, self.size[1]*qj, self.size[2]*qk) for vertex in self.vertices]
        )

# Groups are for putting together Mesh objects
class Group:
    
    def __init__(self, shapes=None, position=None, unit_vectors=None):
        self.shapes = [] if shapes is None else shapes
        self.position = Q([0,0,0]) if position is None else position
        self.unit_vectors = UNIT_QUATERNIONS.copy() if unit_vectors is None else unit_vectors
    
    def render(self, position=Q([0,0,0]), unit_vectors=None, light_vector=Q([0,0,0])):
        unit_vectors = UNIT_QUATERNIONS.copy() if unit_vectors is None else unit_vectors
        for shape in self.shapes:
            if isinstance(shape, Mesh):
                shape.render(position + self.position.morph(*unit_vectors), self.unit_vectors.morph(*unit_vectors), light_vector)
            elif isinstance(shape, Group):
                shape.render(position + self.position.morph(*unit_vectors), self.unit_vectors.morph(*unit_vectors), light_vector)