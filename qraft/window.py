
import math

import pygame

from aquaternion import *

from . import camera as cam

class Window:

    def __init__(self,
        size: tuple[int, int] = (600, 400),
        title: str = 'Window',
        background_color: str = '#16181D',
    ):
        
        # Define size, width, height and create window surface
        self._set_size(size)
        
        self.title = title
        pygame.display.set_caption(self.title)
        
        self.background_color = pygame.Color(background_color)
        
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.k = 0
        
        self.camera = cam.Camera(Q([0,0,0]), UnitVectors(), 60)
        
    def update(self):
        pygame.display.update()
        
    def clear(self):
        self.surface.fill(self.background_color)
    
    def mainloop_events(self, clear_surface=False, update_surface=True, auto_quit=True):
        
        self.clock.tick(self.FPS)
        self.k += 1
        pygame.display.set_caption(f'{self.title} | FPS: {self.clock.get_fps():.2f}')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if auto_quit:
                    pygame.quit()
                return True
            if event.type == pygame.MOUSEWHEEL:
                self.camera.field_of_view -= event.y
        
        if update_surface:
            self.update()
        
        if clear_surface:
            self.clear()
        
    def mainloop(self):
        looping = True
        while looping:
            looping = not bool(self.mainloop_events())


    def _set_size(self, size: tuple[int, int]):
        self.__size = self.__width, self.__height = size
        self.aspect_ratio = self.__width / self.__height
        self.surface = pygame.display.set_mode(self.__size)
    
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self, size):
        self._set_size(size)
    
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, width: int):
        self._set_size((width, self.height))
    
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, height: int):
        self._set_size((self.width, height))
    
    
    def project_vertex(self, camera: cam.Camera, vertex: Quaternion):
        window_width = self.width
        window_height = self.height
        focal_length = camera.focal_length(window_width)
        
        relative_vertex = (vertex - camera.position).unmorphed(*camera.unit_vectors)
        x = (relative_vertex.x * focal_length / (focal_length + relative_vertex.z * window_width / 2) + 1) * window_width / 2
        y = (relative_vertex.y * focal_length / (focal_length + relative_vertex.z * window_height / 2) + 1) * window_height / 2
        
        return (x, y)
    
    def project_vertices(self, relative_vertices: QuaternionArray, focal_length=1):
        window_width = self.width
        window_height = self.height
        
        outside_fov_bools = [vertex.z > -focal_length for vertex in relative_vertices]

        projected_vertices = [
            (
                relative_vertex.x * (focal_length * window_width / 2) / (focal_length + relative_vertex.z) + window_width / 2,
                relative_vertex.y * (focal_length * window_width / 2) / (focal_length + relative_vertex.z) + window_height / 2
            )
            for relative_vertex in relative_vertices
        ]
        
        return projected_vertices, outside_fov_bools
    
    def draw_line(self, point1, point2, color='#00ff00'):
        pygame.draw.aaline(self.surface, color, point1, point2)
    
    def draw_lines(self, vertices: list[tuple[int, int]], color='#00ff00'):
        pygame.draw.aalines(self.surface, color, True, vertices)
    
    def draw_polygon(self, vertices: list[tuple[int, int]], color=pygame.Color(0,80,160), filled=True, width=1):
        pygame.draw.polygon(self.surface, color, vertices, width*(not filled))