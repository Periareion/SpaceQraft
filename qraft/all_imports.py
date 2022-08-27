
import datetime
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from .aquaternion import *

from . import graphics
from . import geometry as gm
from . import utils
from . import environment as env