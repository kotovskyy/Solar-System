import pygame
import os
import math


# TODO 
# rewrite usign better scaling and positioning

SCALE = 1000000
COLORS = {"white" : (255, 255, 255),
          "black" : (0, 0, 0),
          "red" : (255, 0, 0),
          "green" : (0, 255, 0),
          "blue" : (0, 0, 255),
          "grey" : (75, 75, 75)}

class App:
    def __init__(self, PLANETS) -> None:
        self.PLANETS = PLANETS
        self.run = True
        self.WIDTH = 1200
        self.HEIGHT = 900
        self.FPS = 60
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load(os.path.join("solarSystem", "Assets", "background1.jpg"))
        self.background = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.PLANETS_RECT = {planet.name : pygame.Rect(*self._get_planet_position(planet), *planet.get_size()) for planet in self.PLANETS}
        self.ORBITS = dict()
        pygame.display.set_caption("Solar System")

    def _get_planet_position(self, planet):
        xpos = self.WIDTH/2 - planet.width/2 - planet.orbit_radius
        ypos = self.HEIGHT/2 - planet.height/2
        return (xpos, ypos)

    def run_app(self):
        while self.run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            # self.create_orbits()
            keys_pressed = pygame.key.get_pressed()
            self.zoom_handle(keys_pressed)
            # earth_keys_handle(keys_pressed=keys_pressed, earth=earth)

            self._planet_movement()
            self.draw_window()

    def zoom_handle(self, keys_pressed):
        global SCALE
        if keys_pressed[pygame.K_UP]:
            SCALE -= 100000
        if keys_pressed[pygame.K_DOWN]:
            SCALE += 100000
        print(SCALE)

    def draw_window(self):
        self.WIN.blit(self.background, (0, 0))
        pygame.draw.circle(self.WIN, COLORS["red"], (self.WIDTH/2, self.HEIGHT/2), 2, 2)
        for planet in self.PLANETS:
            # if planet.name != 'sun':
                # orb_w = planet.semi_major_axis*2/1000000+planet.prev_pl_rad + planet.prev_pl_orbit
                # orb_h = planet.semi_minor_axis*2/1000000+planet.prev_pl_rad + planet.prev_pl_orbit
                # orb_w = planet.semi_major_axis*2/1000000+planet.orbit_radius
                # orb_h = planet.semi_minor_axis*2/1000000+planet.orbit_radius
                # pygame.draw.ellipse(self.WIN, COLORS["red"], (self.WIDTH/2-orb_w/2, self.HEIGHT/2-orb_h/2, orb_w, orb_h ), 3)
                # pygame.draw.ellipse(self.WIN, COLORS["red"], (self.WIDTH, self.HEIGHT, orb_w, orb_h ), 3)

            self.WIN.blit(planet.planet, (self.PLANETS_RECT[planet.name].x, self.PLANETS_RECT[planet.name].y))
        pygame.display.update()
    
    # orbit's center: c = sqrt(a^2 - b^2)
    # def draw_orbits(self):
    #     for planet in self.PLANETS:
    #         orb_w = planet.semi_major_axis*2/1000000
    #         orb_h = planet.semi_minor_axis*2/1000000-50
    #         c = math.sqrt((planet.semi_major_axis/1000000)**2 - (planet.semi_minor_axis/1000000)**2) 
    #         pygame.draw.ellipse(self.WIN, COLORS["red"], (self.WIDTH/2+c-orb_w/2, self.HEIGHT/2-orb_h/2, orb_w, orb_h ), 3)

    def _planet_movement(self):
        time_unit = 1/4 # day
        prev_pl_orbit = 0
        for planet in self.PLANETS:
            if planet.orbit_radius <= 0:
                continue
            planet_rect = self.PLANETS_RECT[planet.name]
            angle_change = planet.angular_velocity * time_unit
            planet.angle -= angle_change
            planet.orbit_radius = planet.p / (1 + planet.e*math.cos(planet.angle))
            planet.orbit_radius = planet.orbit_radius / SCALE # scale to pixels
            planet.orbit_radius += planet.prev_pl_rad + planet.prev_pl_orbit
            planet.prev_pl_orbit = prev_pl_orbit
            prev_pl_orbit = planet.orbit_radius
            planet_rect.x = planet.orbit_radius * math.cos(planet.angle) + self.WIDTH/2 + planet.width/2
            planet_rect.y = planet.orbit_radius * math.sin(planet.angle) + self.HEIGHT/2 + planet.height/2
    
        
class Planet:
    def __init__(self, name, width, height, orbit_radius, angle, w, e, semimajor, prev_pl_rad=0) -> None:
        self.name = name
        self.width = width
        self.height = height
        self.orbit_radius = orbit_radius
        self.angle = math.radians(angle)
        self.semi_major_axis = semimajor
        self.e = e  # e -- eccentricity
        self.semi_minor_axis = math.sqrt(-1*math.pow(self.semi_major_axis, 2)*(math.pow(self.e, 2)-1))  
        self.p = math.pow(self.semi_minor_axis, 2) / self.semi_major_axis if self.semi_major_axis != 0 else 0 # p -- semi-lactus rectum (km)
        self.angular_velocity = w # radian/day
        self.prev_pl_rad = prev_pl_rad
        self.prev_pl_orbit = 0
        self.planet_image = pygame.image.load(os.path.join("solarSystem", "Assets", f"{self.name}.png"))
        self.planet = pygame.transform.scale(self.planet_image, (self.width, self.height))

    def get_size(self):
        return (self.width, self.height)

def main():

    SUN = Planet('sun', 150, 150, 0, 0, 0, 0, 0)
    MERCURY = Planet('mercury', 50, 50, 130, 0, 0.071425, 0.205630, 57910000, SUN.height)
    VENUS = Planet('venus', 55, 55, 190, 180, 0.027962, 0.006772, 108210000, MERCURY.height)
    EARTH = Planet('earth', 75, 55, 250, 0, 0.017202, 0.0167086, 149598023, VENUS.height)
    # MARS = Planet('mars', 55, 55, 330, 0.9, 70)
    # JUPYTER = Planet('jupyter', 80, 80, 425, 0.5, 120)
    # SATURN = Planet('saturn', 180, 80, 550, 0.7, 240)
    # URANUS = Planet('uranus', 60, 60, 300, 0.2, 200)
    # NEPTUNE = Planet('neptune', 60, 60, 390, 0.2, 290)



    # PLANETS = [SUN, MERCURY, VENUS, EARTH, MARS, JUPYTER, SATURN, URANUS, NEPTUNE]
    PLANETS = [SUN, MERCURY, VENUS, EARTH]
    app = App(PLANETS)
    app.run_app()

if __name__ == "__main__":
    main()