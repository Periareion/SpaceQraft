
from qraft import *

import spacemath as sm

def main(width, height, FPS=60):
    t = 0
    dt = 1
    clock = pygame.time.Clock()

    scene = env.Scene('Scene', width, height, (0.05, 0.05, 0.1, 1))

    camera = env.Camera(Q([0,0,2]), UV.copy(), 60)
    mouse = env.Mouse(width, height)
    keyboard = env.Keyboard()

    scene.set_FOV(camera.field_of_view)

    light_vector = Q([-1,-1,-2])


    stars = sm.bodies.stars.values()
    planets = sm.bodies.planets.values()

    for star in stars:
        star.model = gm.Sphere(radius=4e-4*(star.radius**0.3), color=star.color, vertical_n = 8, horizontal_n = 8)
        scene.objects.append(star.model)
    
    for planet in planets:
        planet.model = gm.Sphere(radius=6e-4*(planet.radius**0.3), color=planet.color, vertical_n = 4, horizontal_n = 6)
        scene.objects.append(planet.model)
        
        planet.path_points = planet.orbit.get_path_points(60, 2 / sm.constants.AU)
        scene.lines.append((planet.path_points, planet.color))
    
    # TODO: make camera follow a planet
    # TODO: maybe come up with a way to perform Hohmann transfers?
    # TODO: planet axis of rotation


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

        for planet in planets:
            planet.update_position(t*10000000)
            planet.model.position = planet.position / sm.constants.AU

        scene.update()
        scene.render(camera, light_vector)

        t += dt / FPS
        clock.tick(FPS); fps = clock.get_fps()
        pygame.display.set_caption(f'{scene.name} (FPS: {fps:.2f}, FOV: {camera.field_of_view})')

        if keyboard.downs[pygame.K_F2]: buffer = utils.get_buffer()

        pygame.display.flip()
        
        if keyboard.downs[pygame.K_F2]: utils.save_screenshot(scene, buffer)

    pygame.quit()

if __name__ == '__main__':
    main(1000, 800, 60)