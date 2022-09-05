
from qraft import *

G = 1

class Planet:

    def __init__(self, name, mass, position, velocity, radius, color=(1,1,1)):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color

        self.sphere = gm.Group([gm.Sphere(radius=radius, color=color, vertical_n=10, horizontal_n=10)])

    def update_position(self, dt, FPS=60):
        self.position += self.velocity * dt / FPS
    
    def update_velocity(self, planets, dt, FPS=60):
        net_acceleration = Q([0,0,0])
        for planet in planets:
            if planet is self:
                continue
            dist = planet.position - self.position
            acceleration = G * planet.mass * (dist * dist.norm**-3)
            net_acceleration += acceleration
        self.velocity += net_acceleration * dt / FPS
    
    def render(self, position, unit_vectors, light_vector):
        self.sphere.position = self.position
        self.sphere.render(position, unit_vectors, light_vector)

def main(width, height, FPS=60):
    t = 0
    dt = 1
    clock = pygame.time.Clock()

    scene = env.Scene('Gravity', width, height, (0.05, 0.05, 0.1, 1))

    camera = env.Camera(Q([0,0,2]), UV.copy(), 60)
    mouse = env.Mouse(width, height)
    keyboard = env.Keyboard()

    scene.set_FOV(camera.field_of_view)

    light_vector = Q([-1,-2,-3])

    sun = Planet("Sun", 1, Q([0,0,0]), Q([0,0,0]), 0.1, (0.8, 0.7, 0.204))
    earth = Planet("Earth", 10**-10, Q([1,0,0]), Q([0,0.7,0]).rotate(qi, 1), 0.03, (0.145, 0.439, 0.804))
    mars = Planet("Mars", 10**-10, Q([1.2,0,0]), Q([0,0.8,0]).rotate(qi, 0), 0.03, (0.804, 0.239, 0.145))
    scene.objects = [sun, mars]

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

        camera.position = earth.position.copy()
        #x = earth.velocity.normalized
        #camera.unit_vectors = QA([x, qk, x*qk])
        z = (earth.position - sun.position).normalized
        x = (earth.velocity.normalized*z).qvector3/z
        camera.unit_vectors = UnitVectors([x, z*x, z])

        #print(camera.unit_vectors)

        for planet in [sun, earth, mars]:
            planet.update_velocity(scene.objects, dt, FPS)
        for planet in [sun, earth, mars]:
            planet.update_position(dt, FPS)

        scene.update()
        scene.render(camera, light_vector)

        t += dt / FPS
        clock.tick(FPS); fps = clock.get_fps()
        pygame.display.set_caption(f'Gravity (FPS: {fps:.2f}, FOV: {camera.field_of_view})')

        if keyboard.downs[pygame.K_F2]: buffer = utils.get_buffer()

        pygame.display.flip()
        
        if keyboard.downs[pygame.K_F2]: utils.save_screenshot(scene, buffer)

    pygame.quit()

if __name__ == '__main__':
    main(800, 600, 60)