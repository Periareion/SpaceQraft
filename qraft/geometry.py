
import weakref

from aquaternion import *

from . import utils
from .entity import Entity


class Group(Entity):
    
    def __init__(self,
        objects: list = None,
        position: Quaternion = None,
        unit_vectors: UnitVectors = None,
    ):
        self.objects = utils.default([], objects)
        super().__init__(position, unit_vectors)
    
    def unpack(self, position=Q([0,0,0]), unit_vectors=UnitVectors(), depth=1):
        self.inherit(position, unit_vectors)
        meshes = []
        for obj in self.objects:
            if isinstance(obj, Mesh):
                mesh = obj
                mesh.inherit(self.true_position, self.true_unit_vectors)
                meshes.append(mesh)
            elif isinstance(obj, Group):
                group = obj
                group.inherit(self.true_position, self.true_unit_vectors)
                meshes.extend(group.unpack(depth=depth+1))
        return meshes


class Mesh(Entity):
    
    #vertices = ()
    #edges = ()
    #faces = ()
    
    def __init__(self,
        position = None,
        unit_vectors = None,
        color='#00AA00',
    ):
        super().__init__(position, unit_vectors)
        self.color = color
        self.triangle_faces = []
        split_polygons = list([list([(face[0], face[i+1], face[i+2]) for i in range(len(face)-2)]) for face in self.faces])
        for triangles in split_polygons:
            for triangle in triangles:
                self.triangle_faces.append(triangle)


class Cuboid(Mesh):

    vertices = ((-1, -1, -1), (-1, -1, 1),
                (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1),
                (1, 1, -1), (1, 1, 1))

    edges = ((0, 4), (1, 5), (2, 6), (3, 7),
             (0, 2), (1, 3), (4, 6), (5, 7),
             (0, 1), (2, 3), (4, 5), (6, 7))

    faces = ((0, 1, 3, 2), (0, 4, 5, 1), (0, 2, 6, 4),
             (7, 5, 4, 6), (7, 6, 2, 3), (7, 3, 1, 5))
    
    def __init__(self,
        position = None,
        unit_vectors = None,
        color='#2178ee',
        size=(1,1,1),
    ):
        super().__init__(position, unit_vectors, color)
        
        self.size = size
        
        self.qvertices = QuaternionArray(
            [0.5*Q(vertex) for vertex in self.vertices]
        ).morphed(self.size[0]*qi, self.size[1]*qj, self.size[2]*qk)


class Icosahedron(Mesh):
    
    def __init__(self,
        radius = None,
        **kwargs,
    ):
        pass


class Sphere(Mesh):
    
    def __init__(self,
        position = None,
        unit_vectors = None,
        color = '#BBDDFF',
        radius = 0.5,
    ):
        self.radius = radius
        self.diameter = 2 * self.radius
        self.volume = 4/3*math.pi*self.radius**3
        self.color = color
        
        super().__init__(position, unit_vectors, color)
        

class UVSphere(Sphere):
    
    """
    Generates a UV sphere mesh
    vertical_n: number of vertical points from one pole to the other
    horizontal_n: number of horizontal points
    """
    
    def __init__(self,
        position = None,
        unit_vectors = None,
        color = '#BBDDFF',
        radius = 0.5,
        vertical_n = 10,
        horizontal_n = 10
    ):

        self.vertices = UVSphere.get_vertices(radius, vertical_n, horizontal_n)
        self.faces = UVSphere.get_faces(vertical_n, horizontal_n)
        
        super().__init__(position, unit_vectors, color, radius)
        
        self.qvertices = QuaternionArray(
            [Q(vertex) for vertex in self.vertices]
        )

    @classmethod
    def vertices_in_row(cls, m, n, row):
        return 1 if (row == 0 or row == m-1) else n
    

    #@classmethod
    #def squares_under_row(cls, m, i):
    #    return UVSphere.vertices_in_row(m, 0, i) == UVSphere.vertices_in_row(m, 0, i+1)
        
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
        return 2 + (m-2)*n # UVSphere.vertex_number(m, n, m-1, 1)

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
                    vertices.append(UVSphere.vertex_position(radius, m, n, i, j))
        
        return vertices
    
    @classmethod
    def number_of_faces(cls, m, n):
        return 2*n*(m-2) # 2*n + (m-3)*2*n

    @classmethod
    def get_faces(cls, m, n):
        faces: list[tuple[float]] = [(0,)]*UVSphere.number_of_faces(m, n)
        current_face_number = 0
        for i in range(m-1):
            for j in range(n):
                if i == 0:
                    vertex0 = UVSphere.vertex_number(m, n, i, j)
                    vertex1 = UVSphere.vertex_number(m, n, i+1, j)
                    vertex2 = UVSphere.vertex_number(m, n, i+1, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                elif i == m-2:
                    vertex0 = UVSphere.vertex_number(m, n, i, j)
                    vertex1 = UVSphere.vertex_number(m, n, i+1, j)
                    vertex2 = UVSphere.vertex_number(m, n, i, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                else:
                    vertex0 = UVSphere.vertex_number(m, n, i, j)
                    vertex1 = UVSphere.vertex_number(m, n, i+1, j)
                    vertex2 = UVSphere.vertex_number(m, n, i+1, j+1)
                    vertex3 = UVSphere.vertex_number(m, n, i, j+1)

                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex1, vertex2)
                    current_face_number += 1
                    faces[current_face_number-1] = (vertex0, vertex2, vertex3)

        return faces