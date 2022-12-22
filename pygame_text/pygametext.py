import pygame
from pygame_texteditor import TextEditor

pygame.init()
screenHeight = 600
screenWidth = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pygame")
pygame.display.get_surface().fill((200, 200, 200))  # background coloring

# parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 500
textAreaWidth = 800


# Instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)
TX.set_line_numbers(True)  # optional 
TX.set_syntax_highlighting(True)  # optional
TX.set_font_size(12)

while True:  # pygame-loop
    # capture input
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    TX.set_colorscheme_from_yaml("C:\\Users\\anton\\Dropbox\\Repositories\\Qraft\\modelling\\theme.yml")
    TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)

    # display editor functionality once per loop

    # update pygame window
    pygame.display.flip()  

