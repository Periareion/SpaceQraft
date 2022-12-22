
from qraft import *

window = Window(title='', size=(600,700))

mouse = peripherals.Mouse()
keyboard = peripherals.Keyboard()

window.renderer.objects = []

import random
def random_hex():
    hex_color = '#'+hex(random.randint(0,16**6-1)).replace('0x', '').zfill(6)
    #print(hex_color)
    return hex_color

group = Group([], [])
v1, v2, v3 = Q([0, 0, 5]), Q([1, 0, 5]), Q([1, -1, 5])
for i in range(100):
    group.shapes.append(
        Mesh([v1.vector3, v2.vector3, v3.vector3], [(0, 1, 2)], random_hex())
    )
    print(v1, v2, v3)
    v1, v2, v3 = v2, v3, v1+qj+qk*random.random()+qi*random.random()

group = Group([Icosasphere(radius=1, k=1)], position=Q([0,0,3]))
window.renderer.objects = [group]
group.save_to_json()

import os

last_modified_timestamp = 0
running = True
while running:
    mouse.update()
    keyboard.update()
    window.camera.movement(mouse, keyboard)
    if (modified_timestamp := os.path.getmtime('group.json')) != last_modified_timestamp:
        last_modified_timestamp = modified_timestamp
        try:
            print("trying to reload mesh")
            temp = window.renderer.objects
            #window.renderer.objects = [Group.load_json('group.json')]
        except Exception as e:
            window.renderer.objects = temp
            print(e)
    
    window.renderer.render()
    
    running = not bool(window.mainloop_events(True))