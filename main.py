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
gold = [229, 169, 11]

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
    obst_points = [(0, 0), (10, 5), (20, 0), (15, 10), (20, 20), (10, 15), (0, 20), (5, 10)]
    obst_surf = py.Surface((20, 20), py.SRCALPHA)
    py.draw.polygon(obst_surf, red, obst_points)
obstacle()

def goal():
    global goal_surf
    goal_points = [(10, 0), (8, 8), (0, 10), (8, 12), (10, 20), (12, 12), (20, 10), (12, 8)]
    goal_surf = py.Surface((20, 20), py.SRCALPHA)
    py.draw.polygon(goal_surf, gold, goal_points)
goal()

gravity = 0.5
player_jumpheight = 10
y_vel = player_jumpheight
jumping = False

bg_1 = gradient(width, height, crimson, black)
bg_2 = gradient(width, height, burn_orange, smoky_brown)

player = player_surf.get_rect(center = (30, 450))
target = goal_surf.get_rect(center = (490, 100))
obstacles = [
    obst_surf.get_rect(center = (0, 445)),
    obst_surf.get_rect(center = (300, 445)),
    obst_surf.get_rect(center = (300, 420)),
    obst_surf.get_rect(center = (300, 395)),
]
for i in range(10):
    obstacles.append(obst_surf.get_rect(center = (25 * (i + 1), 420)))
for i in range(13):
    obstacles.append(obst_surf.get_rect(center = (0, 25 * i - 5)))
for i in range(4):
    obstacles.append(obst_surf.get_rect(center = (0, 25 * (i+15) - 5)))
for i in range(5):
    obstacles.append(obst_surf.get_rect(center = (25 * i + 200, 280)))
platforms = [
    platform_surf.get_rect(center = (200, 400)),
    platform_surf.get_rect(center = (250, 300)),
    platform_surf.get_rect(center = (400, 200)),
    platform_surf.get_rect(center = (450, 350)),
    platform_surf.get_rect(center = (50, 350)),
    platform_surf.get_rect(center = (100, 400))
]
for i in range(5):
    platforms.append(platform_surf.get_rect(center = (100 * i + 50, 465)))
gamestate = 'playing'
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
    screen.blit(background, (0, 0))
    for i in platforms:
        screen.blit(platform_surf, i)
    for i in obstacles:
        screen.blit(obst_surf, i)
    if gamestate == 'playing':
        if (key[py.K_UP] or key[py.K_w] or key[py.K_SPACE]) and jumping == False:
            jumping = True
            y_vel = -1 * player_jumpheight
            player.y += y_vel
        if (key[py.K_LEFT] or key[py.K_a]):
            player.x -= 2
        if (key[py.K_RIGHT] or key[py.K_d]):
            player.x += 2
        if jumping == True:
            if y_vel < 10:
                y_vel += gravity
        for i in platforms:
            if player.colliderect(i):
                jumping = False
                y_vel = player_jumpheight
                player.y -= 10
        for i in obstacles:
            if player.colliderect(i):
                gamestate = 'game_over'
        if player.y > height:
            player.y = 0
        if player.y < 0:
            player.y = height
        if player.x > width * 0.99:
            player.x = 0
        if player.x < 0:
            player.x = width * 0.99
        if player.colliderect(target):
            gamestate = 'win'
    elif gamestate == 'game_over':
        run = False
    elif gamestate == 'win':
        run = False
    screen.blit(player_surf, player)
    screen.blit(goal_surf, target)
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()