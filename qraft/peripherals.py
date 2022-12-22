
import pygame


class Mouse:
    
    def __init__(self, width=600, height=400):
        self.half_width, self.half_height = width // 2, height // 2

        self.pressed = pygame.mouse.get_pressed(5)
        
        self.toggle_focus = False
        self.focused = False
        self.position = None
        self.delta_position = (0, 0)
        self.update()
    
    def update(self):
        
        new_pressed = pygame.mouse.get_pressed(5)
        self.downclicks = tuple((not self.pressed[i] and new_pressed[i] for i in range(5)))
        self.upclicks = tuple((self.pressed[i] and not new_pressed[i] for i in range(5)))
        self.pressed = new_pressed
        
        if self.downclicks[2]:
            self.focused = not self.focused
            if self.focused:
                self.hide()
                self.position = pygame.mouse.get_pos()
            else:
                self.show()
        
        if self.focused:
            new_position = pygame.mouse.get_pos()
            self.delta_position = new_position[0]-self.position[0], new_position[1]-self.position[1]
            pygame.mouse.set_pos(self.position)

    def hide(self):
        pygame.mouse.set_visible(False)

    def show(self):
        pygame.mouse.set_visible(True)


class Keyboard:

    def __init__(self):
        self.state = pygame.key.get_pressed()
    
    def update(self):
        new_state = pygame.key.get_pressed()
        self.downs = pygame.key.ScancodeWrapper((now and not then for (now, then) in zip(new_state, self.state)))
        self.ups = pygame.key.ScancodeWrapper((not now and then for (now, then) in zip(new_state, self.state)))
        self.state = new_state
