
from aquaternion import *

from . import utils
from .entity import Entity

import json


class ShapeWrapper(Entity):
    
    def __init__(self,
        shape,
        position: Quaternion = None,
        unit_vectors: UnitVectors = None,
    ):
        self.shape = shape
        super().__init__(position, unit_vectors)


class Group(Entity):
    
    def __init__(self,
        shapes: list = None,
        subgroups: list = None,
        position: Quaternion = None,
        unit_vectors: UnitVectors = None,
    ):
        self.shapes = [] if shapes is None else shapes
        self.subgroups = [] if subgroups is None else subgroups
        super().__init__(position, unit_vectors)
    
    def __repr__(self):
        return f"Group(\n    shapes={self.shapes} \n    subgroups={self.subgroups})"
    
    def unpack(self, position=Q([0,0,0]), unit_vectors=UnitVectors(), depth=1):
        self.inherit(position, unit_vectors)
        wrapped_shapes = []
        
        # Yank the leaf nodes out of the tree and and put it in a list so that it remembers the whole branch
        for subgroup in self.subgroups:
            wrapped_shapes.extend(subgroup.unpack(self.true_position, self.true_unit_vectors, depth=depth+1))
        
        for shape in self.shapes:
            wrapped_shape = ShapeWrapper(shape)
            wrapped_shape.inherit(self.true_position, self.true_unit_vectors)
            wrapped_shapes.append(wrapped_shape)
        
        return wrapped_shapes
    
    @staticmethod
    def load_group_object(group_object):
        shapes = list([Mesh.load_mesh_object(shape) for shape in group_object["shapes"]])
        subgroups = list([Group.load_group_object(group) for group in group_object["subgroups"]])
        position = Q(group_object["position"])
        unit_vectors = UnitVectors([Q(vector) for vector in group_object["unit_vectors"]])
        return Group(shapes, subgroups, position, unit_vectors)
    
    @staticmethod
    def load_json(filename: str):
        file = open(filename)
        group_object = json.load(file)
        file.close()
        group = Group.load_group_object(group_object)
        print(group)
        return group
    
    def save_to_json(self, filename="test.json"):
        file = open(filename, "w")
        dict_object = self.dictionarify()
        json.dump(dict_object, file, indent=4)
        file.close()
    
    def dictionarify(self):
        dict_object = {
            "type": "group",
            "shapes": list([shape.dictionarify() for shape in self.shapes]),
            "subgroups": list([subgroup.dictionarify() for subgroup in self.subgroups]),
            "position": self.position.vector3,
            "unit_vectors": list([unit_vector.vector3 for unit_vector in self.unit_vectors.unit_vectors])
        }
        return dict_object

# TODO: dynamic line which is actually a tetragon and changes width based in distance
# TODO: mesh editor where you control individual vertices and it's connections


class Mesh:
    
    def __init__(self,
        static_vertices: list = None,
        faces: list = None,
        color = None,
    ):
        self.static_vertices = [] if static_vertices is None else static_vertices
        self.static_vertices_q = QuaternionArray(list([Q(vertex) for vertex in self.static_vertices]))
        self.faces = [] if faces is None else faces
        self.color = '#BBDDFF' if color is None else color
        self.triangle_faces = []
        split_polygons = list([list([(face[0], face[i+1], face[i+2]) for i in range(len(face)-2)]) for face in self.faces])
        for triangles in split_polygons:
            for triangle in triangles:
                self.triangle_faces.append(triangle)
                
        if not hasattr(self, 'dynamic_vertices'):
            self.dynamic_vertices = QuaternionArray([Q(vertex) for vertex in self.static_vertices])
    
    def __repr__(self):
        return f"Mesh(\n    vertices={self.static_vertices}\n    faces={self.faces})"
    
    @staticmethod
    def load_mesh_object(mesh_object):
        vertices = mesh_object["vertices"]
        faces = mesh_object["faces"]
        color = mesh_object["color"]
        return Mesh(vertices, faces, color)
    
    def dictionarify(self):
        dict_object = {
            "type": "mesh",
            "vertices": self.static_vertices,
            "faces": self.faces,
            "color": self.color
        }
        return dict_object

class Lines(Mesh):
    
    def __init__(self,
        vertices: list[tuple[float, float, float]],
        closed = False,
        width = 0.01,
        **kwargs,
    ):
        if closed:
            vertices.append(vertices[0])
        
        self.faces = []
        for i in range(len(vertices)-1):
            j = 4*i
            self.faces.append((j, j+2, j+3, j+1))
        
        super().__init__(vertices, self.faces, **kwargs)
        
        self.width = width
        self.radius = self.width/2
    
    def set_dynamic_vertices(self, camera_position):
        self.dynamic_vertices = QuaternionArray([])
        for i in range(len(self.static_vertices_q)-1):
            vertex0, vertex1 = self.static_vertices_q[i]-camera_position, self.static_vertices_q[i+1]-camera_position
            rel_vertex1 = vertex1-vertex0
            displacement_normal = Q.cross(vertex0, rel_vertex1)
            displacement_normal.norm = self.radius
            self.dynamic_vertices.array.extend([
                vertex0 + displacement_normal,
                vertex0 - displacement_normal,
                vertex1 + displacement_normal,
                vertex1 - displacement_normal,
            ])

class Cuboid(Mesh):

    static_vertices = ((-1, -1, -1), (-1, -1, 1),
                (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1),
                (1, 1, -1), (1, 1, 1))

    edges = ((0, 4), (1, 5), (2, 6), (3, 7),
             (0, 2), (1, 3), (4, 6), (5, 7),
             (0, 1), (2, 3), (4, 5), (6, 7))

    faces = ((0, 1, 3, 2), (0, 4, 5, 1), (0, 2, 6, 4),
             (7, 5, 4, 6), (7, 6, 2, 3), (7, 3, 1, 5))
    
    def __init__(self,
        size = (1,1,1),
        **kwargs,
    ):
        super().__init__(self.static_vertices, self.faces, **kwargs)
        
        self.size = size
        
        self.dynamic_vertices = QuaternionArray(
            [0.5*Q(vertex) for vertex in self.static_vertices]
        ).morphed(self.size[0]*qi, self.size[1]*qj, self.size[2]*qk)


class Icosahedron(Mesh):
    
    phi = (1+math.sqrt(5))/2
    r = math.sqrt(1+phi**2)
    
    static_vertices = (
        (0,phi,1), (0,-phi,1), (0,-phi,-1), (0,phi,-1),
        (1,0,phi), (1,0,-phi), (-1,0,-phi), (-1,0,phi),
        (phi,1,0), (-phi,1,0), (-phi,-1,0), (phi,-1,0),
    )
    
    faces = (
        (0,7,4), (0,4,8), (0,8,3), (0,3,9), (0,9,7),
        (5,3,8), (5,6,3), (5,2,6), (5,11,2), (5,8,11),
        (1,11,4), (1,4,7), (1,7,10), (1,10,2), (1,2,11),
        (10,9,6), (9,10,7), (6,9,3), (10,6,2), (4,11,8), 
    )
    
    def __init__(self,
        radius = 1,
        **kwargs,
    ):
        self.radius = radius
        
        super().__init__(self.static_vertices, self.faces, **kwargs)
        
        self.dynamic_vertices = QuaternionArray(
            [Q(vertex).normalized*self.radius for vertex in self.static_vertices]
        )


class Sphere(Mesh):
    
    def __init__(self,
        radius = 1,
        static_vertices = None,
        faces = None,
        **kwargs,
    ):
        self.radius = radius
        self.diameter = 2 * self.radius
        self.volume = 4/3*math.pi*self.radius**3
        
        super().__init__(static_vertices, faces, **kwargs)


class Icosasphere(Sphere):
    
    def __init__(self,
        radius = 1,
        k = 2,
        **kwargs,
    ):
        self.icosahedron = Icosahedron(radius)
        vertices = self.icosahedron.dynamic_vertices.array
        faces = list(self.icosahedron.faces)
        n = len(vertices)
        for _ in range(k):
            new_faces = []
            for face in faces:
                v0, v2, v4 = [vertices[i] for i in face]
                v1, v3, v5 = (v0+v2).normalized*radius, (v2+v4).normalized*radius, (v4+v0).normalized*radius
                vertices.extend([v1, v3, v5])
                new_faces.extend([
                    (face[0], n+0, n+2),
                    (face[1], n+1, n+0),
                    (face[2], n+2, n+1),
                    (n+0, n+1, n+2),
                ])
                n += 3
                
            faces = new_faces
        self.dynamic_vertices = QuaternionArray(vertices)
        self.faces = faces
        self.static_vertices = list([vertex.vector3 for vertex in self.dynamic_vertices])
        super().__init__(radius, self.static_vertices, self.faces, **kwargs)


class UVSphere(Sphere):
    
    """
    Generates a UV sphere mesh
    vertical_n: number of vertical points from one pole to the other
    horizontal_n: number of horizontal points
    """
    
    def __init__(self,
        radius = 1,
        vertical_n = 10,
        horizontal_n = 10,
        **kwargs,
    ):

        self.static_vertices = UVSphere.get_vertices(radius, vertical_n, horizontal_n)
        self.faces = UVSphere.get_faces(vertical_n, horizontal_n)
        
        super().__init__(radius, self.static_vertices, self.faces, **kwargs)
        
        self.dynamic_vertices = QuaternionArray(
            [Q(vertex) for vertex in self.static_vertices]
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