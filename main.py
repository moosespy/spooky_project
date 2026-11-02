import pygame as py
import sys

py.init()
font = py.font.SysFont(None, 36)
width = 500
height = 500
screen = py.display.set_mode((width, height), py.DOUBLEBUF)

black = [0, 0, 0]
crimson = [139, 0, 0]
dark_purple = [26, 3, 0]

def gradient(w, h, col_top, col_bot):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), col_top)
    bg_surf.set_at((0, 1), col_bot)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf

bg_1 = gradient(width, height, crimson, black)


background = bg_1
clock = py.time.Clock()
run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    screen.blit(background, (0, 0))
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()