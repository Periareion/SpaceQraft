
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

try:
    from .aquaternion import *
    from . import colors
except ImportError:
    from aquaternion import *
    import colors


def get_camera_unit_vectors(camera_direction, camera_up):
    camera_direction.normalize()
    camera_up.normalize()
    return QA([camera_direction, camera_up*camera_direction, camera_up])


def surface_normal(vertices):
    vertex0, vertex1, vertex2 = vertices
    return ((vertex1 - vertex0)*(vertex2 - vertex0)).qvector.normalized


def triangle_light_factor0(vertices, light_vector, ambient_light):
    light_vector.normalize()
    if len(vertices) != 3:
        raise IndexError(f"Need 3 vertices to make a three dimensional normal vector.")
    p1, p2, p3 = vertices
    normal_vector = ((p2 - p1)*(p3 - p2)).qvector.normalized
    chord = (light_vector + normal_vector).norm
    anomaly = 2 * math.asin(chord / 2)
    return ambient_light + (1 - ambient_light)*max(0, math.cos(anomaly))


def triangle_light_factor(vertices: tuple[Quaternion], light_vector: Quaternion, ambient_light: float):
    light_vector.normalize()
    if len(vertices) != 3:
        raise IndexError(f"Need 3 vertices to make a three dimensional normal vector.")
    p1, p2, p3 = vertices
    normal_vector = ((p2 - p1)*(p3 - p2)).qvector.normalized
    return ambient_light*(1 + Quaternion.dot(-normal_vector, light_vector))


class Vertex:

    def __init__(self, position):
        self.position = position
        self.screen_position()

    def screen_position(self, camera_position, camera_unit_vectors, width, height, FOV_V, FOV_H):
        
        absolute_relative_position = self.position - camera_position
        #relative_position = absolute_relative_position.morph(*camera_unit_vectors)
        h_angle_camera_point = math.atan2()



class Triangle:

    def __init__(self, vertices):
        self.vertices
        self.surface_normal()
    
    def surface_normal(self):
        self.normal = surface_normal(self.vertices)


def sort_triangles(camera, vertices, projected_vertices, triangles, order):
    for i, triangle in enumerate(triangles):
        triangle_vertices = (vertices[j] for j in triangle)
        normal = surface_normal(triangle_vertices)

        camera_ray = triangle_vertices[0] - camera
        distance = camera_ray.norm
        camera_ray_normalized = camera_ray / distance

        screen_x = []
        screen_y = []