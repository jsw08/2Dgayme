import pygame as np
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

        self.frames = {}
        for mode in ["idle", "walk", "hit", "die"]:
            for x in range(eval(f"num_of_{mode}_frames")):
                print(mode, x)



    def draw(self, screen):
        pass

    def animate(self, dT):
        pass
        