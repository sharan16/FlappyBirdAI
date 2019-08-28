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
    bird.update()
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

main()
