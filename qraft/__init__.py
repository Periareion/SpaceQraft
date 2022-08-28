
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import datetime

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from . import graphics
from . import geometry as gm
from . import environment as env

from .aquaternion import *