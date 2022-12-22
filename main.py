
from qraft import *

window = Window(title='Qraft', size=(800,600))

group = Group([
    #Cuboid(),
    ],
    [
        Group([
            Icosasphere(radius=0.2, k=0),
        ],
        position=Q([1.5,0,0])),
        Group([
            UVSphere(radius=0.2, color='#0066CC'),
        ],
        position=Q([-1.5,0,0]))
    ],
    position=Q([0,0,3]))

    #Lines([(0,0,3), (0,1,3), (2,1,3), (-1,2,3), (2,2,3)], True, 0.05)
mouse = peripherals.Mouse()
keyboard = peripherals.Keyboard()

window.renderer.objects = [group]

running = True
while running:
    group.unit_vectors.rotate(qi+qj, 0.0)
    mouse.update()
    keyboard.update() 
    window.camera.movement(mouse, keyboard)
    
    window.renderer.render()
    
    running = not bool(window.mainloop_events(True))