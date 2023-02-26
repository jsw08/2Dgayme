import pygame as pg

from files.player import *

player = Player(10,10)
pg.init()
screen = pg.display.set_mode((600,600),pg.RESIZABLE)
playing = True
pg.display.set_caption("template")



while playing:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            playing = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                playing = False
        pg.event.pump()

        mx, my = pg.mouse.get_pos()
        screen.fill((0,0,0))
        pg.draw.circle(screen,(255,255,255),(mx,my),5)
        pg.display.flip()

pg.quit()

# omg edits