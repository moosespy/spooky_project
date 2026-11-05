import pygame as py
import sys

py.init()
font = py.font.SysFont(None, 36)
width = 500
height = 500
screen = py.display.set_mode((width, height), py.DOUBLEBUF)

black = [0, 0, 0]
red = [255, 0, 0]
crimson = [139, 0, 0]
dark_purple = [26, 3, 0]
burn_orange = [255, 69, 0]
smoky_brown = [15, 5, 4]
blue = [0, 0, 255]
gray = [128, 128, 128]

def gradient(w, h, col_top, col_bot):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), col_top)
    bg_surf.set_at((0, 1), col_bot)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf
def play_stand():
    global player_surf
    body_points = [(0, 0), (20, 0), (20, 20), (0, 20)]
    player_surf = py.Surface((20, 20), py.SRCALPHA)
    py.draw.polygon(player_surf, blue, body_points)
play_stand()

def platform():
    global platform_surf
    platform_points = [(0, 0), (100, 0), (100, 10), (0, 10)]
    platform_surf = py.Surface((100, 10), py.SRCALPHA)
    py.draw.polygon(platform_surf, gray, platform_points)
platform()

def obstacle():
    global obst_surf
    obst_points = [(0, 0), ((10, 1), (20, 0), (19, 10), (20, 20), (10, 19), (0, 20), (1, 10))]
    obst_surf = py.Surface((20, 20), py.SRCALPHA)
    py.draw.polygon(obst_surf, red, obst_points)
obstacle()

gravity = 0.5
player_jumpheight = 10
y_vel = player_jumpheight
jumping = False

bg_1 = gradient(width, height, crimson, black)
bg_2 = gradient(width, height, burn_orange, smoky_brown)

player = player_surf.get_rect(center = (250, 450))
spike = obst_surf.get_rect(center = (250, 400))
platforms = [
    platform_surf.get_rect(center = (250, 465)),
    platform_surf.get_rect(center = (100, 405)),
    platform_surf.get_rect(center = (250, 300)),
    platform_surf.get_rect(center = (400, 200)),
    platform_surf.get_rect(center = (450, 450))
]

background = bg_2
clock = py.time.Clock()
run = True
while run:
    key = py.key.get_pressed()
    player.y += y_vel
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_1:
                background = bg_1
            elif event.key == py.K_2:
                background = bg_2
    if (key[py.K_UP] or key[py.K_w] or key[py.K_SPACE]) and jumping == False:
        jumping = True
        y_vel = -1 * player_jumpheight
        player.y += y_vel
    if (key[py.K_LEFT] or key[py.K_a]):
        player.x -= 2
    if (key[py.K_RIGHT] or key[py.K_d]):
        player.x += 2
    screen.blit(background, (0, 0))
    for i in platforms:
        screen.blit(platform_surf, i)
    if jumping == True:
        if y_vel < 10:
            y_vel += gravity
    for i in platforms:
        if player.colliderect(i):
            jumping = False
            y_vel = player_jumpheight
            player.y -= 10
    if player.y > height:
        player.y = 0
    if player.y < 0:
        player.y = height
    screen.blit(player_surf, player)

    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()