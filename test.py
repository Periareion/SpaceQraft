
from qraft import *

def main(width, height, FPS=60):
    t = 0
    dt = 1/FPS
    clock = pygame.time.Clock()

    scene = env.Scene('Qraft', width, height)

    camera = env.Camera(Q([0, 0, 3]), UV.copy(), 60)
    mouse = env.Mouse(width, height)
    keyboard = env.Keyboard()

    scene.set_FOV(camera.field_of_view)

    light_vector = Q([1,-1.5,-2])

    def colored_amogus(color):
        
        # Make video with Pixies' song "Allison".
        amogus = gm.Group([gm.Group([
            gm.Cuboid((0.65, 0, 0),(0.65, 0.5, 0.55),color),
            gm.Cuboid((0.5, -0.3, 0),(0.5, 0.2, 0.4),color),
            gm.Cuboid((0.3, 0, 0.15),(0.5, 0.4, 0.25),color),
            gm.Cuboid((0.3, 0, -0.15),(0.5, 0.4, 0.25),color),
            gm.Cuboid((0.7, 0.25, 0),(0.3, 0.2, 0.4),(0.3,0.7,0.9)),
            gm.Cuboid((0.8, 0.25, -0.1),(0.05, 0.21, 0.1),(0.8,0.9,1))],
            position=[-0.5,0,0])])
        return amogus
        
    amogi = gm.Group([
        gm.Group([(colored_amogus((0.85,0.9,0.2)))], [0,0,1], UV.copy().rotate(qj, math.pi/2)),
        gm.Group([(colored_amogus((0.1,0.9,0.2)))], [0,0,-1]),
        gm.Group([(colored_amogus((0.9,0.1,0.2)))], [0,0,-2]),
        gm.Group([(colored_amogus((0.1,0.1,0.9)))], [0,0,0], UV.copy().rotate(qk, math.pi/2)),
        ])
    
    amogi = gm.Group([
        gm.Group([(colored_amogus((0.85,0.9,0.2)))], [0,0,1], UV.copy().rotate(qj, math.pi/2)),
        gm.Group([(colored_amogus((0.1,0.9,0.2)))], [0,0,-1]),
        gm.Group([(colored_amogus((0.9,0.1,0.2)))], [0,0,-2]),
        gm.Group([(colored_amogus((0.1,0.1,0.9)))], [0,0,0], UV.copy().rotate(qk, math.pi/2)),
        ])

    sphere = gm.Group([gm.Sphere(radius=1)])
    scene.objects = [amogi]

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEWHEEL:
                camera.field_of_view += -event.y
                scene.set_FOV(camera.field_of_view)

        mouse.update()
        keyboard.update()
        camera.update(mouse, keyboard)

        scene.update()
        scene.render(camera, light_vector)

        t += dt
        clock.tick(FPS); fps = clock.get_fps()
        pygame.display.set_caption(f'Qraft (FPS: {fps:.2f}, FOV: {camera.field_of_view})')

        if keyboard.downs[pygame.K_F2]: buffer = glReadPixels(0, 0, *scene.window.get_size(), GL_RGBA, GL_UNSIGNED_BYTE)

        pygame.display.flip()
        
        if keyboard.downs[pygame.K_F2]: pygame.image.save(
            pygame.image.fromstring(buffer, scene.window.get_size(), "RGBA"), f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg")

    pygame.quit()

if __name__ == "__main__":
    main(800, 600, 60)
