
from qraft import *

def main(width, height, FPS=60):
    t = 0
    dt = 1
    clock = pygame.time.Clock()

    scene = env.Scene('Scene', width, height, (0.05, 0.05, 0.1, 1))

    camera = env.Camera(Q([0,0,2]), UV.copy(), 60)
    mouse = env.Mouse(width, height)
    keyboard = env.Keyboard()

    scene.set_FOV(camera.field_of_view)

    light_vector = Q([-1,-2,-3])

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEWHEEL:
                camera.field_of_view -= event.y
                scene.set_FOV(camera.field_of_view)

        mouse.update()
        keyboard.update()
        camera.update(mouse, keyboard)

        # Do stuff here

        scene.update()
        scene.render(camera, light_vector)

        t += dt / FPS
        clock.tick(FPS); fps = clock.get_fps()
        pygame.display.set_caption(f'{scene.name} (FPS: {fps:.2f}, FOV: {camera.field_of_view})')

        if keyboard.downs[pygame.K_F2]: buffer = utils.get_buffer(scene)

        pygame.display.flip()
        
        if keyboard.downs[pygame.K_F2]: utils.save_screenshot(scene, buffer)

    pygame.quit()

if __name__ == '__main__':
    main(800, 600, 60)