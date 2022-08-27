
from qraft import *

def main(width, height, FPS=60):
    t = 0
    dt = 1/FPS
    clock = pygame.time.Clock()

    scene = env.Scene('Qraft', width, height)

    camera = env.Camera(Q([0, 0, 3]), UNIT_QUATERNIONS.copy(), 60)
    mouse = env.Mouse(width, height)
    keyboard = env.Keyboard()

    scene.set_FOV(camera.field_of_view)

    light_vector = Q([1,-1.5,-2])

    sphere = gm.Group([gm.Sphere(radius=1)])
    scene.objects = [sphere]

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
