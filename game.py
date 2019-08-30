import pygame
import time
import neat
import os
import random
import math
pygame.font.init()
WIN_W = 570
WIN_H = 800

IMGS_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
FONT_STAT = pygame.font.SysFont("comicsans",50)
class Base:
    VEL = 5
    WIDTH = IMG_BASE.get_width()
    IMG = IMG_BASE

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1-=self.VEL
        self.x2-=self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
class Pipe():

    GAP = 200
    VEL = 5

    def __init__(self, x):

        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
        self.PIPE_BOTTOM = IMG_PIPE

        self.passed = False

        self.set_height()

    def set_height(self):

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        return b_point or t_point

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
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird,pipes,base,score):
    win.blit(IMG_BG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    text = FONT_STAT.render("Score: " + str(score),1,(255,255,255))
    win.blit(text, (WIN_W-10-text.get_width(),10))
    bird.draw(win)
    pygame.display.update()

def main():
    win =  pygame.display.set_mode((WIN_W,WIN_H))
    base = Base(730)
    pipes = [Pipe(700)]
    bird = Bird(230,350)
    run = True
    add_pipe = False
    score = 0
    while run:
        pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                print('pressed')
        for i, pipe in enumerate(pipes):
            if (pipe.collide(bird)):
                pass
            if (pipe.x + pipe.PIPE_TOP.get_width()) < 0:
                pipes.pop(i)
            if not pipe.passed and pipe.x<bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        
        if add_pipe:
            score +=1
            pipes.append(Pipe(700))
            add_pipe = False
  
        base.move()
        draw_window(win, bird,pipes,base,score)
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