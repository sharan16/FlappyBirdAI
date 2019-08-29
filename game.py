import pygame
import time
import neat
import os
import random
import math

WIN_W = 600
WIN_H = 800

IMGS_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png')))]
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.y_top = 0
        self.y_bottom = 0
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE,False,True)
        self.PIPE_BOTTOM = IMG_PIPE

        self.passed = false
        self.set_height()
    def set_height(self)
        self.height = random.randrange(50,400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom - self.heigh + self.GAP
    def move(self)
        self.x -= self.VEL
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.y_top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.y_bottom))
    def collide(self,bird):
        bird_mask = bird.mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return (t_point or b_point)


class Bird:
    IMGS = IMGS_BIRD
    MAX_ROT = 25
    VEL_ROT = 20
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0 
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def update(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 2*(self.tick_count**2)
        if d > 16:
            d = 16
        elif d<0:
            d = -2
        self.y += d
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0 
        self.height = self.y
    
    def draw(self,win): # Drawing the bird
        self.img_count += 1
        self.img = self.IMGS[math.floor(self.img_count/5)]

        if self.tilt < -80:
            self.img = self.IMGS[1]
            self.img_count = 0
        
        if self.img_count > 13:
            self.img_count = 0

        rotated_img = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_img,new_rect.topleft)
    
    def mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win,bird):
    win.blit(IMG_BG,(0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    win =  pygame.display.set_mode((WIN_W,WIN_H))
    bird = Bird(200,200)
    run = True
    while run:
        pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(win, bird)
    pygame.quit()
    quit()

def run(config_file_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_file_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))

# local_dir = os.path.dirname(__file__)
# config_file_path = os.path.join(local_dir,'neatconfig.txt')
# run(config_file_path)
main()