import os
import math
import pygame

# TODO
# separate scale for planets size

COLORS = {"white" : (255, 255, 255),
          "black" : (0, 0, 0),
          "red" : (255, 0, 0),
          "green" : (0, 255, 0),
          "blue" : (0, 0, 255),
          "grey" : (75, 75, 75)}


class SolarSystem:
    def __init__(self, PLANETS):
        self.WIDTH = 900
        self.HEIGHT = 900
        self.FPS = 60
        self.time_unit = 1/24 # day
        self.SCALE = 1
        self.km_per_pixel = 204444.44
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)
        self.run = True
        self.background_image = pygame.image.load(os.path.join("solarSystem", "Assets", "background1.jpg"))
        self.background = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Solar System")

        self.PLANETS = PLANETS
        self.PLANETS_RECTS = {planet.name : pygame.Rect((0, 0), (planet.width, planet.height)) for planet in self.PLANETS}

    def execute(self):
        while self.run:
            self.km_per_pixel = 204444.44 * self.SCALE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys_pressed = pygame.key.get_pressed()
            self.zoom_handle(keys_pressed)
            self.planets_movement()
            self.draw_window()

    def zoom_handle(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            self.SCALE -= 0.01
        if keys_pressed[pygame.K_DOWN]:
            self.SCALE += 0.01
        print(f"SCALE : {self.SCALE}")

    def pygame_to_cartesian(self, coords):
        # center of Cartesian coordinate system
        # in our case looks like this:
        center = (self.WIDTH/2, self.HEIGHT/2)
        new_x = round(coords[0] - center[0])
        new_y = round(center[1] - coords[1])
        return (new_x, new_y)
    
    def cartesian_to_pygame(self, coords):
        center = (self.WIDTH/2, self.HEIGHT/2)
        new_x = round(coords[0] + center[0])
        new_y = round(center[1]-coords[1])
        return (new_x, new_y)

    def real_to_window_cart(self, coords):
        new_x = round(coords[0] / self.km_per_pixel)
        new_y = round(coords[1] / self.km_per_pixel)
        return (new_x, new_y)

    def draw_orbits(self):
        for planet in self.PLANETS:
            if planet.name == 'sun':
                continue
            window_coords = self.real_to_window_cart((-1*planet.perihelion, planet.semiminor))
            window_coords = self.cartesian_to_pygame(window_coords)
            rect_w = 2*planet.semimajor/self.km_per_pixel
            rect_h = 2*planet.semiminor/self.km_per_pixel
            orbit_rect = pygame.Rect((window_coords), (rect_w+planet.width/2, rect_h))
            pygame.draw.rect(self.WIN, COLORS['red'], orbit_rect, 4)
            pygame.draw.ellipse(self.WIN, COLORS['red'], orbit_rect, 2)

    def planets_movement(self):
        for planet in self.PLANETS:
            if planet.name == 'sun':
                continue
            planet_rect = self.PLANETS_RECTS[planet.name]
            angle_change = planet.angular_vel * self.time_unit
            planet.angle -= angle_change
            planet.semilatusrectum = math.pow(planet.semiminor, 2) / planet.semimajor
            planet.dist_from_sun = planet.semilatusrectum / (1 + planet.eccentricity * math.cos(planet.angle))
            real_dist = round(planet.dist_from_sun / self.km_per_pixel)
            print(f"DIST_FROM_SUN : {real_dist}")
            planet_rect.x = real_dist * math.cos(planet.angle)
            planet_rect.y = real_dist * math.sin(planet.angle)


    def draw_window(self):
        self.WIN.blit(self.background, (0, 0))
        pygame.draw.circle(self.WIN, COLORS["red"], (self.WIDTH/2, self.HEIGHT/2), 2, 2)
        self.draw_orbits()
        for planet in self.PLANETS:
            self.WIN.blit(planet.planet, (self.WIDTH/2 - self.PLANETS_RECTS[planet.name].x - planet.width/2, self.HEIGHT/2 - self.PLANETS_RECTS[planet.name].y - planet.height/2))
        pygame.display.update()

class Planet:
    def __init__(self, name, width, height, or_period, e, semimajor, perihelion, angle):
        self.name = name
        self.width = width
        self.height = height    
        self.orbital_period = or_period
        self.angle = math.radians(angle)
        self.angular_vel = 0 if self.orbital_period == 0 else 2 * math.pi / self.orbital_period
        self.eccentricity = e
        self.semimajor = semimajor
        self.perihelion = perihelion
        self.dist_from_sun = 0
        self.focus_to_center = self.semimajor - self.perihelion
        self.semiminor = math.sqrt(math.pow(self.semimajor, 2) - math.pow(self.focus_to_center, 2))
        self.semilatusrectum = 0
        self.planet_image = pygame.image.load(os.path.join("solarSystem", "Assets", f"{self.name}.png"))
        self.planet = pygame.transform.scale(self.planet_image, (self.width, self.height))


def main():
    SUN = Planet('sun', 150, 150, 0, 0, 0, 0, 0)
    MERCURY = Planet('mercury', 50, 50, 87.9691, 0.240846, 57.91e6, 46.00e6, 0)
    VENUS = Planet('venus', 55, 55, 583.92, 0.006772, 108.21e6, 107.48e6, 90)
    EARTH = Planet('earth', 50, 50, 365.256, 0.0167086, 149598023, 147098450, 0)
    MARS = Planet('mars', 50, 50, 686.980, 0.0934, 227939366, 206650000, 180)
    JUPYTER = Planet('jupyter', 70, 70, 4332.59, 0.0489, 778477399.54866, 740599218.68742, 270)
    SATURN = Planet('saturn', 112, 50, 10755.70, 0.0565, 1433.53e6, 1352.55e6, 0)
    URANUS = Planet('uranus', 55, 55, 30688.5, 0.04717, 2870971632.0501, 2735561623.4073, 90)
    NEPTUNE = Planet('neptune', 55, 55, 60195, 0.008678, 4498407971.949, 4459512525.567, 270)

    PLANETS = [SUN, MERCURY, VENUS, EARTH, MARS, JUPYTER, SATURN, URANUS, NEPTUNE]
    app = SolarSystem(PLANETS)
    app.execute()

if __name__ == "__main__":
    main()