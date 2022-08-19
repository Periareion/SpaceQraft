
import math

from OpenGL.GL import *
from OpenGL.GLU import *

try:
    from .aquaternion import *
    from . import colors
except ImportError:
    from aquaternion import *
    import colors

def drop_vertex(position, color):
    glColor3fv(color)
    glVertex3fv(position)


def draw_line(p1, p2, color, width=1):
    glLineWidth(GLfloat(width))
    glBegin(GL_LINES)
    drop_vertex(p1, color)
    drop_vertex(p2, color)
    glEnd()


def triangle_light_factor(vertices, light_vector, ambient_light):
    if len(vertices) != 3:
        raise IndexError(f"Need 3 vertices to make a three dimensional normal vector.")
    p1, p2, p3 = vertices
    normal_vector = ((p2 - p1)*(p3 - p2)).qvector.normalized
    chord = (light_vector.normalized + normal_vector).norm
    anomaly = 2 * math.asin(chord / 2)
    return ambient_light + (1 - ambient_light)*max(0, math.cos(anomaly))


def draw_triangle(vertices=[Q([-5,-5,0]), Q([5,-5,0]), Q([0,5,0])], color=(1,1,1), light_vector=Q([0,0,0])):
    if len(vertices) != 3:
        raise IndexError(f"Can't draw triangle with {len(vertices)} vertices.")
    
    light_factor = triangle_light_factor(vertices, light_vector, 0.3)
    
    for qvector in vertices:
        drop_vertex(qvector.vector3, tuple(map(lambda x: x*light_factor, color)))


def draw_tetragon(vertices, color=(1,1,1), light_vector=Q([0,0,1])):
    if len(vertices) != 4:
        raise IndexError(f"Can't draw tetragon with {len(vertices)} vertices.")
    
    draw_triangle([vertices[0], vertices[1], vertices[2]], color, light_vector)
    draw_triangle([vertices[0], vertices[2], vertices[3]], color, light_vector)

