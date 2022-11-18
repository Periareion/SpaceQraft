
from qraft import *

window = Window(title='Cube', size=(800,600))
camera = window.camera

group = Group([
    UVSphere(vertical_n=10, horizontal_n=20, color = '#CCEEFF')
    ], position=Q([0,0,3]))

cube1 = Cuboid(Q([0,0,5]), size=(2,1,2))
cube2 = Cuboid(Q([0,1,5]), size=(2,1,2), color='#ff8000')

renderer = Renderer(window, camera)

mouse = Mouse()
keyboard = Keyboard()

running = True
while running:
    
    group.unit_vectors.rotate(Q([1,1,1]), 0.02)
    
    mouse.update()
    keyboard.update()
    camera.movement(mouse, keyboard)
    
    renderer.render([group])
    
    running = not bool(window.mainloop_events(True))