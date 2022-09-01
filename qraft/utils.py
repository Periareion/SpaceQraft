
import datetime

import pygame
from OpenGL.GL import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE

def get_buffer(scene):
    return glReadPixels(0, 0, *scene.window.get_size(), GL_RGBA, GL_UNSIGNED_BYTE)

def save_screenshot(scene, buffer):
    pygame.image.save(
        pygame.image.fromstring(buffer, scene.window.get_size(), "RGBA"),
        f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")