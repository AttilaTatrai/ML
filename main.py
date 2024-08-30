import pygame
import neat
import time
import os
import random

#size of the game window
WIN_WIDTH = 550
WIN_HEIGHT = 800
FPS = 30

#counters and default settings
score = 0
generation = 0
population = 0

#score display on screen
pygame.font.init()
START_FONT = pygame.font.SysFont("comicons", 40)

#images path settings
#must be in img dir
sBirdPath1 = os.path.join("img", "bird1.png")
sBirdPath2 = os.path.join("img", "bird2.png")
sBirdPath3 = os.path.join("img", "bird3.png")
sBasePath = os.path.join("img", "base.png")
sBgPath = os.path.join("img", "bg.png")
sPipePath = os.path.join("img", "pipe.png")

#set screen size
screen_size = (WIN_WIDTH, WIN_HEIGHT)

#load images into an array
#enlarge the images by 2 (scale2x)
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(sBirdPath1)),
             pygame.transform.scale2x(pygame.image.load(sBirdPath2)),
             pygame.transform.scale2x(pygame.image.load(sBirdPath3))]

BASE_IMG = pygame.transform.scale2x(pygame.image.load(sBasePath))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(sPipePath))
BG_IMG = pygame.transform.scale2x(pygame.image.load(sBgPath))


#creating bird class
class Brid:
    #set up parameters
    IMGS = BIRD_IMGS
    ANIMATION_TIME = 3 #delay between animations

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.tilt = 0
        self.tick_count = 0 #movement counter
        self.vel = 0 #speed , velocity
        self.height = self.y
        self.img_count = 0 #image counter for wing animation
        self.img = self.IMGS[0] #start with the first bird image
    #end of function __init__

    def jump(self):
        self.vel = -9 #chaning bird pisition verticaly
        self.tick_count = 0
        self.height = self.y
    #end of jump function

    #bird moving
    def move(self):
        self.tick_count +=1

        delta = self.vel * self.tick_count +1,5 * self.tick_count**2

        if delta >= 16:
            delta = 16
        if delta < 0:
            delta -=2

        #change position of the bird
        self.y = self.y + delta
    #end of move function

    def draw(self, win):
        self.img_count +=1 #wich image to show

        if self.img_count == self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        if self.img_count == self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        if self.img_count == self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
            self.img_count = 0

        #copy image to the window screen
        win.blit(self.img, (self.x, self.y))
    #end of draw function

    #get mask collosion detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    #end of get_mask

#pipe class creation
class Pipe:
    GAP = 200   #space between pipes
    VEL = 7     # speed of pipes

    #params setup
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        #a pipe object contains 2 pipes
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False #does the bird passed the pipe?
        self.set_height()
    #end of function __init__

    def set_height(self):
        self.height = random.randrange(30,550)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    #end of set_height function

#asd