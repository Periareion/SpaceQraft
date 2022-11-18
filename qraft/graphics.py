
import pygame

from aquaternion import *

from . import geometry


class Edge:
    
    def __init__(self, vertex1: Quaternion, vertex2: Quaternion, color):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.color = color


def light_factor(surface_normal: Quaternion, light_vector: Quaternion = Q([0,0,1]), ambient_light: float = 0.3):
    light_vector.normalize()
    return ambient_light + (1 - ambient_light)*max(0, Quaternion.dot(-surface_normal, light_vector))


class Triangle:
    
    def __init__(self, vertices: list[Quaternion], projected_vertices: list[tuple[int, int]], focal_vector, color, light_vector: Quaternion = Q([1,2,3])):
        self.vertices = vertices
        self.middle_point = sum(vertices) / 3
        self.distance_to_camera = (self.middle_point + focal_vector).norm
        self.vertex_distance_sum = sum([(vertex + focal_vector).norm for vertex in vertices])
        
        self.normal = Quaternion.cross(vertices[1] - vertices[0], vertices[2] - vertices[0]).normalized
        self.light_factor = light_factor(self.normal, light_vector)
        
        self.color = pygame.Color(color)
        self.apparent_color = pygame.Color(int(self.color.r*self.light_factor), int(self.color.g*self.light_factor), int(self.color.b*self.light_factor))
        
        self.projected_vertices = projected_vertices
    
    @classmethod
    def split_polygon(cls, vertices: list[Quaternion], proj_vertices: list[tuple[int, int]], *args, **kwargs):
        return [cls([vertices[0], vertices[i+1], vertices[i+2]], [proj_vertices[0], proj_vertices[i+1], proj_vertices[i+2]], *args, **kwargs) for i in range(len(vertices)-2)]

    def render(self, window):
        window.draw_polygon(self.projected_vertices, self.apparent_color, filled=True)
        window.draw_lines(self.projected_vertices, self.apparent_color)

    def __repr__(self):
        return f"Triangle({self.vertices})"
    
    __str__ = __repr__


class Renderer:
    
    def __init__(self, window, camera):
        self.window = window
        self.camera = camera
    
    def create_triangles(self, mesh):
        focal_length = self.camera.focal_length
        focal_vector = focal_length*qk
        absolute_focal_vector = focal_vector.morphed(*self.camera.unit_vectors)
        light_vector = Q([1,2,3]).unmorphed(*self.camera.unit_vectors)
        triangles = []
        vertices = mesh.qvertices.morphed(*mesh.true_unit_vectors) + mesh.true_position
        relative_vertices = (vertices + -(self.camera.position + absolute_focal_vector)).unmorphed(*self.camera.unit_vectors)
        projected_vertices, mesh.fov_bools = self.window.project_vertices(relative_vertices, focal_length)
        for triangle_face in mesh.triangle_faces:
            if True not in [mesh.fov_bools[i] for i in triangle_face]: # No vertices are in the field of view
                continue
            triangle = Triangle(
                [relative_vertices[i] for i in triangle_face],
                [projected_vertices[i] for i in triangle_face],
                focal_vector,
                mesh.color,
                light_vector,
            )
            if False in [-2*self.window.width < triangle.projected_vertices[j][0] < 3*self.window.width and 
                            -2*self.window.height < triangle.projected_vertices[j][1] < 3*self.window.height
                            for j in range(3)]:
                continue
            if (Quaternion.dot((triangle.middle_point + focal_vector).normalized, triangle.normal.normalized) > 0):
                continue
            triangles.append(triangle)
        return triangles
    
            #face_triangles = Triangle.split_polygon(
            #    [relative_vertices[i] for i in face],
            #    [projected_vertices[i] for i in face],
            #    self.focal_vector,
            #    mesh.color,
            #    Q([1,2,3]).unmorphed(*self.camera.unit_vectors)
            #)
            #for i in reversed(range(len(face_triangles))):
    
    def render(self, objects):
        if not objects:
            # Don't try to render anything if there are no meshes to render
            return
        
        objects = geometry.Group(objects)
        meshes = objects.unpack()
        
        triangles = []
        
        for mesh in meshes:
            triangles.extend(self.create_triangles(mesh))
        
        distances = [(i, triangle.vertex_distance_sum) for i, triangle in enumerate(triangles)]
        
        try:
            order = list(zip(*sorted(distances, key=lambda x: x[1], reverse=True)))[0]
        except IndexError as e:
            #print(e)
            # There are no triangles to draw (they're outside the field of view)
            return

        for i in order:
            triangles[i].render(self.window)
        
        
        