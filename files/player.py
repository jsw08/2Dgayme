import pygame as pg
import time as t
import random as r

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vmax = 1
        self.width = self.height = 48

        self.cur_mode = "walk" # changes to "idle", "walk", "hit" or "die"
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
                    for direction in ["front", "right", "back"]:
                        self.frames[f"{mode}_{direction}_{x+1}"] = pg.image.load(f"{self.player_path}{mode}_{direction} ({x+1}).png")
                else:
                    self.frames[f"{mode}_{x+1}"] = pg.image.load(f"{self.player_path}{mode} ({x+1}).png")


    def draw(self, screen):
        if self.cur_mode != "die":
            img_blit = eval(f"self.frames['{self.cur_mode}_{self.cur_direction}_{int(self.cur_frame+1)}']")
        else:
            img_blit = eval(f"self.frames['{self.cur_mode}_{int(self.cur_frame+1)}']")
        screen.blit(img_blit,(self.x, self.y))

    def animate(self):
        if t.perf_counter() > self.animate_perf + 0.1:
            self.cur_frame = (self.cur_frame + 1) % (eval(f"self.num_of_{self.cur_mode}_frames"))
            self.animate_perf = t.perf_counter()
        
    def move(self, keys, dT):
        if keys[pg.K_w]:
            self.vy = min(self.vy + 0.1, self.vmax)
            self.y += self.vy * dT