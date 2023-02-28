import pygame as pg
import numpy as np
import time as t
import random as r
from perlin_noise import PerlinNoise
pg.init()
pg.font.init()

#CONFIG#
plot_world_gen = False # uses matplotlib (install with pip3 first)
seed = 1
octaves = 15
width_world = 100
height_world = 100
########


grid_size = 16 # how many pixels width and height a tile is


def generate_world(width_world, height_world, seed, octaves):
    noise = PerlinNoise(octaves=octaves, seed=seed)

    world_gen = np.zeros((height_world,width_world),dtype='float')
    for i in range(height_world):
        for j in range(width_world):
            world_gen[j][i] = noise([i/width_world, j/height_world])

    if plot_world_gen:
        import matplotlib.pyplot as plt
        plt.imshow(world_gen)
        plt.show()  

    world = np.zeros((height_world, width_world),dtype="int")
    for i in range(height_world):
        for j in range(width_world):
            world[j][i] = 1 # change this later for if's with world_gen

    world_rotation = np.zeros((height_world, width_world),dtype="int")
    for i in range(height_world):
        for j in range(width_world):
            world_rotation[j][i] = r.randint(0,3) # rotation 0: up, 1: right, 2: down, 3: left

    return world, world_rotation

def load_images():
    images = {} # pictures stored as {"1":pg.surface16x16x32 etc.}
    
    images_path = "ground/"
    images_to_load = [] # all images are .png
    for i in range(44):
        images_to_load.append(str(i))

    for img in images_to_load:
        images[img] = pg.image.load(f"{images_path}{img}.png")
        
    return images

def scale_images(images, scale):
    scaled_images = {}
    for img in images.keys():
        scaled_images[img] = [pg.transform.rotate(pg.transform.scale(images[img], (
                int(scale * grid_size),
                int(scale * grid_size))), -angle) for angle in range(0, 360, 90)]

    return scaled_images

def draw_world(screen, world, world_rotation, scrollx, scrolly, scale, scaled_images):
    screen = screen
    screen_size = screen.get_size()
    for x in range(max(0, int(abs(scrollx) / (grid_size * scale))), min(world.shape[1],
                                                                        int(int((abs(scrollx) + screen_size[0]) / (
                                                                                grid_size * scale) + 1) + np.ceil(
                                                                            (abs(scrollx) + screen_size[0]) / (
                                                                                        grid_size * scale) % 1)))):
        for y in range(max(0, int(abs(scrolly) / (grid_size * scale))), min(world.shape[0],
                                                                            int(int((abs(scrolly) + screen_size[1]) / (
                                                                                    grid_size * scale) + 1) + np.ceil(
                                                                                (abs(scrolly) + screen_size[1]) / (
                                                                                        grid_size * scale) % 1)))):
            block = world[y, x]
            orientation = world_rotation[y, x]
            x_grid_scale = round(x * grid_size * scale) + scrollx
            y_grid_scale = round(y * grid_size * scale) + scrolly

            

            screen.blit(scaled_images[str(block)][orientation], (x_grid_scale, y_grid_scale))

def handle_keys(keys_list, dT, scrollx, scrolly):
    speed = 0.3 * dT
    if keys_list[pg.K_w]:
        scrolly += speed
    if keys_list[pg.K_a]:
        scrollx += speed
    if keys_list[pg.K_s]:
        scrolly -= speed
    if keys_list[pg.K_d]:
        scrollx -= speed

    scrollx = min(scrollx, 0)
    scrolly = min(scrolly, 0)

    return scrollx, scrolly

scrollx = 0
scrolly = 0
scale = 1

images = load_images()
scaled_images = scale_images(images,scale)

screen = pg.display.set_mode((500,500), pg.RESIZABLE, pg.HWSURFACE)
playing = True
pg.display.set_caption("Tile level editor")

world, world_rotation = generate_world(width_world, height_world, seed, octaves)

keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_r]
keys_list = {}

for i in keys:
    keys_list[i] = False

dT = 0
clock = pg.time.Clock()

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

        if e.type == pg.MOUSEWHEEL:
            scale += e.y / 2
            scale = min(max(scale, 0.5), 5)
            print(scale)
            scaled_images = scale_images(images, scale)

        
        pg.event.pump()

    scrollx, scrolly = handle_keys(keys_list, dT, scrollx, scrolly)

    screen.fill((0,0,0))
    draw_world(screen, world, world_rotation, scrollx, scrolly, scale, scaled_images)
    pg.display.flip()
    dT = clock.tick()

pg.font.quit()
pg.quit()


