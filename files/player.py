import pygame as pg
import time as t
import random as r
import numpy as np

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vmax = 1.25
        self.vacc = 0.1 # velocity acceleration
        self.width = self.height = 48

        self.rect = pg.Rect((self.x, self.y), (self.width, self.height))
        self.speed = 0.3

        self.cur_mode = "idle" # changes to "idle", "walk", "hit" or "die"
        self.cur_frame = 0 # from 0-5/0-3/0-2 depending on self.cur_mode
        self.cur_direction = "right"

        self.animate_perf = -1 # perf counter for going to next frame

        # constant variables
        self.num_of_idle_frames = 6
        self.num_of_walk_frames = 6
        self.num_of_hit_frames = 4
        self.num_of_die_frames = 3

        self.player_path = "player_frames/"
        self.frames = {}
        for mode in ["idle", "walk", "hit", "die"]:
            for x in range(eval(f"self.num_of_{mode}_frames")): #walk_right_2
                if mode != "die":
                    for direction in ["front", "right", "left", "back"]:
                        if direction == "left":
                            src = pg.image.load(f"{self.player_path}{mode}_right ({x+1}).png")
                            src = pg.transform.flip(src, True, False)
                            self.frames[f"{mode}_{direction}_{x+1}"] = src
                        else:
                            self.frames[f"{mode}_{direction}_{x+1}"] = pg.image.load(f"{self.player_path}{mode}_{direction} ({x+1}).png")
                else:
                    self.frames[f"{mode}_{x+1}"] = pg.image.load(f"{self.player_path}{mode} ({x+1}).png")


    def draw(self, screen):
        if self.cur_mode != "die":
            img_blit = eval(f"self.frames['{self.cur_mode}_{self.cur_direction}_{int(self.cur_frame+1)}']")
        else:
            img_blit = eval(f"self.frames['{self.cur_mode}_{int(self.cur_frame+1)}']")
        screen.blit(img_blit,(self.rect.x, self.rect.y))

    def animate(self):
        if t.perf_counter() > self.animate_perf + 0.1:
            self.cur_frame = (self.cur_frame + 1) % (eval(f"self.num_of_{self.cur_mode}_frames"))
            self.animate_perf = t.perf_counter()
        
    def move(self, keys, dT):
        if self.cur_mode != "hit" or self.cur_mode != "die":
            pos = pg.math.Vector2(self.rect.x, self.rect.y)

            up = keys[pg.K_w] #or keys[pg.K_UP]
            down = keys[pg.K_s] #or keys[pg.K_DOWN]
            left = keys[pg.K_a] #or keys[pg.K_LEFT]
            right = keys[pg.K_d] #or keys[pg.K_RIGHT]

            self.cur_mode = "idle"
            if up or down or left or right:
                self.cur_mode = "walk"
                if up and not down and not left and not right:
                    self.cur_direction = "back"
                elif down and not up and not left and not right:
                    self.cur_direction = "front"
                elif right and not left and not down and not up:
                    self.cur_direction = "right"
                elif left and not right and not down and not up:
                    self.cur_direction = "left"

            if up:
                self.vy = max(self.vy - self.vacc, -self.vmax)
            if down:
                self.vy = min(self.vy + self.vacc, self.vmax)
            if left:
                self.vx = max(self.vx - self.vacc, -self.vmax)
            if right:
                self.vx = min(self.vx + self.vacc, self.vmax)

            self.vx *= 0.8
            self.vy *= 0.8
            # print(self.vx, self.vy)

            move = pg.math.Vector2(right - left, down - up)
            if move.length_squared() > 0:
                move.scale_to_length(self.speed * dT)
                move.x *= abs(self.vx)
                move.y *= abs(self.vy)
                pos += move  
                self.rect.topleft = round(pos.x), round(pos.y)

    def hit(self, keys):
        if keys[pg.K_SPACE]:
            self.cur_mode = "hit"
            self.cur_frame = 0