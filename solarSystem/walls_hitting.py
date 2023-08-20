import pygame
import os
import random

WIDTH, HEIGHT = 900, 900
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

COLORS = {"white" : (255, 255, 255),
          "black" : (0, 0, 0),
          "red" : (255, 0, 0),
          "green" : (0, 255, 0),
          "blue" : (0, 0, 255),
          "grey" : (75, 75, 75)}

SUN_IMAGE = pygame.image.load(os.path.join("solarSystem", "Assets", "sun.png"))
EARTH_IMAGE = pygame.image.load(os.path.join("solarSystem", "Assets", "earth.png"))

SUN = pygame.transform.scale(SUN_IMAGE, (100, 100))
EARTH = pygame.transform.scale(EARTH_IMAGE, (75, 55))

PLANET_SIZE = {'sun' : (100, 100),
               'earth' : (55, 55)}

EARTH_VELOCITY = 3

MAIN_BOARD = pygame.Rect(50, 50, *(800, 800))

def draw_window(sun, earth):
    WIN.fill(color=COLORS["grey"])
    pygame.draw.rect(WIN, COLORS['white'], MAIN_BOARD)
    WIN.blit(EARTH, (earth.x, earth.y))
    WIN.blit(SUN, (sun.x, sun.y))
    pygame.display.update()

def earth_keys_handle(keys_pressed, earth):
    if keys_pressed[pygame.K_UP] and earth.y - EARTH_VELOCITY > 45: # UP
        earth.y -= EARTH_VELOCITY
    if keys_pressed[pygame.K_DOWN] and earth.y + EARTH_VELOCITY <= 850-PLANET_SIZE["earth"][1]+2: # DOWN
        earth.y += EARTH_VELOCITY
    if keys_pressed[pygame.K_LEFT] and earth.x - EARTH_VELOCITY >  35: # LEFT
        earth.x -= EARTH_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and earth.x + EARTH_VELOCITY <= 850-PLANET_SIZE["earth"][0]+10: # RIGHT
        earth.x += EARTH_VELOCITY

BORDERS = { 'top' : 45, 
            'right' : 850-PLANET_SIZE["earth"][1]+2,
            'bottom' : 850-PLANET_SIZE["earth"][0]+10,
            'left' : 35 }

X_VEL, Y_VEL = 4, 3
previous_hit = ''

def handle_jumping(earth):
    global X_VEL, Y_VEL, previous_hit

    if ((earth.x + X_VEL) <= BORDERS["left"]) and (previous_hit != 'left'):
        X_VEL *= -1
        previous_hit = 'left'
    if ((earth.x + X_VEL) >= BORDERS["right"]) and (previous_hit != 'right'):
        X_VEL *= -1
        previous_hit = 'right'
    if ((earth.y + Y_VEL) <= BORDERS['top']) and (previous_hit != 'top'):
        Y_VEL *= -1
        previous_hit = 'top'
    if ((earth.y + Y_VEL) >= BORDERS['bottom']) and (previous_hit != 'bottom'):
        Y_VEL *= -1 
        previous_hit = 'bottom'

    earth.x += X_VEL
    earth.y += Y_VEL    


def main():
    earth_coords = (random.randint(BORDERS["left"], BORDERS["right"]), random.randint(BORDERS["top"], BORDERS["bottom"]))
    sun = pygame.Rect(400, 400, *PLANET_SIZE['sun'])
    #earth = pygame.Rect(412.5, 572.5, *PLANET_SIZE["earth"])
    earth = pygame.Rect(*earth_coords, *PLANET_SIZE["earth"])
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        # earth_keys_handle(keys_pressed=keys_pressed, earth=earth)
        handle_jumping(earth=earth)
        draw_window(sun, earth)


    pygame.quit()

if __name__ == "__main__":
    main()