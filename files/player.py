import pygame as pg
import time as t
import random as r

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = self.height = 48

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
        pass

    def animate(self, dT):
        pass
        