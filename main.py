import pygame as pg
from files.player import *

player = Player(10,10)
pg.init()

screen = pg.display.set_mode((600,600),pg.RESIZABLE)
pg.display.set_caption("template")

playing = True
keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
keys_list = {}

for i in keys:
    keys_list[i] = False

clock = pg.time.Clock()
dT = 0 # delta time

while playing:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            playing = False

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                playing = False
            for i in keys_list:
                if i == e.key: 
                    keys_list[i] = True   

        if e.type == pg.KEYUP:
            for i in keys_list:
                if i == e.key: 
                    keys_list[i] = False   

        pg.event.pump()

    screen.fill((0, 0, 0))

    # Player
    player.animate()
    player.move(keys_list, dT)
    player.draw(screen)

    pg.display.flip()

    dT = clock.tick(60)

pg.quit()