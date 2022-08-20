
import math

try:
    from .aquaternion import *
    from .utils import validate_types
    from . import graphics
except ImportError:
    from aquaternion import *
    from utils import validate_types
    import graphics

class Polygon:
    
    # Don't call Polygon
    def initialize(self, n, vertices):
        Polygon.check_vertices(n, vertices)
        self.vertices = vertices
    
    @classmethod
    def check_vertices(cls, n, vertices):
        if len(vertices) != n:
            raise IndexError(f"Polygon must have {n} vertices. ({vertices})")
        if not validate_types(vertices, Quaternion):
            raise TypeError("Vertices must be Quaternion instances.")


class Triangle(Polygon):
    n = 3
    
    def __init__(self, vertices, color=(1,1,1)):
        super().initialize(self.n, vertices, color)


class Tetragon(Polygon):
    n = 4
    
    def __init__(self, vertices, color=(1,1,1)):
        super().initialize(self.n, vertices, color)


class Mesh:
    
    def __init__(self, position):
        self.position = Q(position)

    def render(self, position=Q([0,0,0]), unit_vectors=UNIT_QUATERNIONS.copy(), light_vector=Q([0,0,0])):
        qvertices = QA([(vertex + self.position).morph(*unit_vectors) for vertex in self.qvertices])
        for face in self.faces:
            match len(face):
                case 3:
                    graphics.draw_triangle(
                        [(qvertices[vertex] + position) for vertex in face],
                        self.color,
                        light_vector)
                case 4:
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
        self.volume = math.prod(size)
        self.color = color
        
        self.qvertices = QuaternionArray(
            [0.5*Q(vertex).morph(self.size[0]*qi, self.size[1]*qj, self.size[2]*qk) for vertex in self.vertices]
        )


class Sphere(Mesh):

    def __init__(self,
                 position=(0,0,0),
                 radius=0.5,
                 color=(1,1,1),
                 vertical_n=10,
                 horizontal_n=10):
        super().__init__(position)

        self.radius = radius
        self.diameter = 2*self.radius
        self.volume = 4/3*math.pi*self.radius**3
        self.color = color

        self.vertices = Sphere.get_vertices(radius, vertical_n, horizontal_n)
        print(self.vertices)
        self.faces = Sphere.get_faces(vertical_n, horizontal_n)
        self.qvertices = QuaternionArray(
            [Q(vertex) for vertex in self.vertices]
        )

    @classmethod
    def vertices_in_row(cls, m, n, row):
        return 1 if (row == 0 or row == m-1) else n
    

    #@classmethod
    #def squares_under_row(cls, m, i):
    #    return Sphere.vertices_in_row(m, 0, i) == Sphere.vertices_in_row(m, 0, i+1)
        
    @classmethod
    def vertex_number(cls, m, n, i, j):
        if i == 0:
            return 0

        elif i == m-1:
            return 1 + (i-1)*n
        
        else:
            return 1 + (i-1)*n + (j % n)
    
    @classmethod
    def number_of_vertices(cls, m, n):
        return 2 + (m-2)*n # Sphere.vertex_number(m, n, m-1, 1)

    @classmethod
    def vertex_position(cls, radius, m, n, i, j):
        latitude = i/(m-1) * math.pi
        z = radius * math.cos(latitude)
        
        longitude = j/n * math.tau
        w = math.sqrt(max(0, radius**2 - z**2))
        x = w * math.cos(longitude) # (radius**2 - z**2 - y**2)**0.5
        y = w * math.sin(longitude) # math.sqrt(max(0, radius**2 - z**2 - x**2))

        return (x, y, z)

    @classmethod
    def get_vertices(cls, radius, m, n):
        m = max(2, m)
        n = max(3, n)

        vertices = []
        for i in range(m):
            if i == 0:
                vertices.append((0,0,radius))
            elif i == m-1:
                vertices.append((0,0,-radius))
            else:
                for j in range(n):
                    vertices.append(Sphere.vertex_position(radius, m, n, i, j))
        
        return vertices
    
    @classmethod
    def number_of_faces(cls, m, n):
        return 2*n*(m-2) # 2*n + (m-3)*2*n

    @classmethod
    def get_faces(cls, m, n):
        faces: list[tuple[float]] = [(0,)]*Sphere.number_of_faces(m, n)
        current_face_number = 0
        for i in range(m-1):
            for j in range(n):
                if i == 0:
                    vertex0 = Sphere.vertex_number(m, n, i, j)
                    vertex1 = Sphere.vertex_number(m, n, i+1, j)
                    vertex2 = Sphere.vertex_number(m, n, i+1, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                elif i == m-2:
                    vertex0 = Sphere.vertex_number(m, n, i, j)
                    vertex1 = Sphere.vertex_number(m, n, i+1, j)
                    vertex2 = Sphere.vertex_number(m, n, i, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                else:
                    vertex0 = Sphere.vertex_number(m, n, i, j)
                    vertex1 = Sphere.vertex_number(m, n, i+1, j)
                    vertex2 = Sphere.vertex_number(m, n, i+1, j+1)
                    vertex3 = Sphere.vertex_number(m, n, i, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex2, vertex3)

        return faces

print(Sphere.vertex_number(8, 8, 7, 0))

# Groups are for putting together Mesh objects
class Group:
    
    def __init__(self, shapes=None, position=None, unit_vectors=None):
        self.shapes = [] if shapes is None else shapes
        self.position = Q([0,0,0]) if position is None else Q(position)
        self.unit_vectors = UNIT_QUATERNIONS.copy() if unit_vectors is None else unit_vectors
    
    def render(self, position=Q([0,0,0]), unit_vectors=None, light_vector=Q([0,0,0])):
        unit_vectors = UNIT_QUATERNIONS.copy() if unit_vectors is None else unit_vectors
        for shape in self.shapes:
            if isinstance(shape, Mesh):
                shape.render(position + self.position.morph(*unit_vectors), self.unit_vectors.morph(*unit_vectors), light_vector)
            elif isinstance(shape, Group):
                shape.render(position + self.position.morph(*unit_vectors), self.unit_vectors.morph(*unit_vectors), light_vector)