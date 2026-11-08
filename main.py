import pygame as py
import sys
import random

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

restart_text = font.render("You won! Press 'r' to restart.", True, black)
game_over_text = font.render("You hit an obstacle. Press 'r' to restart.", True, black)

particles = []

def draw_particle():
    x = random.randint(0, width)
    y = random.randint(500, 520)
    vel_x = random.uniform(-0.5, 0.5)
    vel_y = random.uniform(-2.1, -4.4)
    radius = random.uniform(1, 3)
    return [[x, y], [vel_x, vel_y], radius]

def gradient(w, h, col_top, col_bot):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), col_top)
    bg_surf.set_at((0, 1), col_bot)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf
def draw_player():
    global player_surf
    body_points = [(0, 3), (3, 0), (20, 0), (20, 20), (1, 20), (0, 19)]
    eye_points = [(17, 3), (14, 2), (16, 7)]
    player_surf = py.Surface((20, 20), py.SRCALPHA)
    py.draw.polygon(player_surf, blue, body_points)
    py.draw.polygon(player_surf, black, eye_points)
draw_player()

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

def triangle():
    global tri_surf
    tri_points = [(0, 5), (10, 10), (10, 0)]
    tri_surf = py.Surface((10, 10), py.SRCALPHA)
    py.draw.polygon(tri_surf, black, tri_points)
triangle()

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

player = player_surf.get_rect(center = (30, 451))
target = goal_surf.get_rect(center = (490, 100))
obstacles = [
    obst_surf.get_rect(center = (0, 445)),
    obst_surf.get_rect(center = (300, 445)),
    obst_surf.get_rect(center = (300, 420)),
    obst_surf.get_rect(center = (300, 395)),
    obst_surf.get_rect(center = (0, 0))
]
for i in range(10):
    obstacles.append(obst_surf.get_rect(center = (25 * (i + 1), 420)))
for i in range(13):
    obstacles.append(obst_surf.get_rect(center = (0, 25 * i - 5)))
for i in range(4):
    obstacles.append(obst_surf.get_rect(center = (0, 25 * (i+15) - 5)))
for i in range(16):
   obstacles.append(obst_surf.get_rect(center = (25 * i + 125, 245)))
for i in range(5):
    obstacles.append(obst_surf.get_rect(center = (125, 25 * i + 295)))
for i in range(20):
    obstacles.append(obst_surf.get_rect(center = (25 * i, 495)))

spear = tri_surf.get_rect(center = (450, 50))
float_platform = platform_surf.get_rect(center = (275, 50))
fplat_limit1, fplat_limit2, fplat_dir = 100, 400, 'left'

platforms = [
    platform_surf.get_rect(center = (200, 400)),
    platform_surf.get_rect(center = (250, 300)),
    platform_surf.get_rect(center = (400, 200)),
    platform_surf.get_rect(center = (450, 350)),
    platform_surf.get_rect(center = (50, 350)),
    platform_surf.get_rect(center = (125, 250)),
    platform_surf.get_rect(center = (200, 150)),
]
for i in range(5):
    platforms.append(platform_surf.get_rect(center = (100 * i + 50, 465)))

gamestate = 'playing'
background = bg_2
clock = py.time.Clock()
run = True
while run:
    key = py.key.get_pressed()
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
    screen.blit(tri_surf, spear)
    screen.blit(platform_surf, float_platform)
    for _ in range(1):
        particles.append(draw_particle())
    new_particles = []
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        if particle[0][1] <= height:
            new_particles.append(particle)
            position = (int(particle[0][0])), int(particle[0][1])
            radius = int(particle[2])
            py.draw.circle(screen, black, position, radius)
    particles = new_particles
    if gamestate == 'playing':
        player.y += y_vel
        if (key[py.K_UP] or key[py.K_w] or key[py.K_SPACE]) and jumping == False:
            jumping = True
            y_vel = -1 * player_jumpheight
            player.y += y_vel
        if (key[py.K_LEFT] or key[py.K_a]):
            player.x -= 2
        if (key[py.K_RIGHT] or key[py.K_d]):
            player.x += 2
        if (key[py.K_g]):
            player.x = 250
            player.y = 5
        if jumping == True:
            if y_vel < 10:
                y_vel += gravity
        for i in platforms:
            if player.colliderect(i):
                jumping = False
                y_vel = player_jumpheight
                player.bottom = i.top
        if player.colliderect(float_platform):
            jumping = False
            y_vel = player_jumpheight
            player.bottom = float_platform.top
        for i in obstacles:
            if player.colliderect(i):
                gamestate = 'game_over'
        spear.x -= 5
        if spear.x < 0:
            spear.x = width
            spear.y = random.randint(0, 500)
        if fplat_dir == 'left':
            float_platform.x -= 3
            if float_platform.x <= fplat_limit1:
                fplat_dir = 'right'
        elif fplat_dir == 'right':
            float_platform.x += 3
            if float_platform.x >= fplat_limit2:
                fplat_dir = 'left'
        if player.y > height:
            player.y = 0
        if player.y < 0:
            player.y = height
        if player.x > width - 1:
            player.x = 1
        if player.x < 1:
            player.x = width - 1
        if player.colliderect(target):
            gamestate = 'win'
        if player.colliderect(spear):
            gamestate = 'game_over'
    elif gamestate == 'game_over':
        screen.blit(game_over_text, (1, 1))
        if (key[py.K_r]):
            gamestate = 'playing'
            player.x = 30
            player.y = 449
    elif gamestate == 'win':
        screen.blit(restart_text, (1, 1))
        if (key[py.K_r]):
            gamestate = 'playing'
            player.x = 30
            player.y = 450
    screen.blit(player_surf, player)
    screen.blit(goal_surf, target)
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()