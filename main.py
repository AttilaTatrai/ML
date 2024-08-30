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
class Bird:
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

    #move pipes on x axis
    def move(self):
        self.x -= self.VEL
        #end of move funtcion

    #draw the 2 pipes
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x, self.top))
        win.blit(self.PIPE_BOTTOM,(self.x, self.bottom))
    #end of draw function

    #collosion detection
    def collide(self, bird):
        #get the mask of the objects to check
        #a mask is a 1bit version of the givenobject
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        #check the distance between objects
        top_offset = (self.x - bird.x, self.top - bird.y)
        bottom_offset = (self.x - bird.x, self.bottom - bird.y)

        #is there any overlapping between masks?
        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        #if so, then birdy hits 1 of the pipes
        if t_point or b_point:
            return True
        #otherwise collosion detected
        return False
    #end of function collide
#end of class pipe

#Base class
class Base:
    VEL =  7
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    #setting up params
    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

        #off the screen? shows up on the right
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    #end of move funciton

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
#end of class Base

def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0,0)) #background drawing

    #draw all the pipes
    for pipe in pipes:
        pipe.draw(win)

    #show score
    pipe_passed = START_FONT.render("Score:  "+ str(score), 1,(255,255,255))
    win.blit(pipe_passed,(5,5))

    base.draw(win)#ground drawing
    bird.draw(win) #bird drawing
    pygame.display.update() #screen updtaing
#end of draw_window function


def run_game():
    pygame.init() #setting up the game engine
    pygame.display.set_caption("Super Birds 2024")

    base = Base(730) #creating the ground object
    bird = Bird(230,350) #creating bird object
    pipes = [Pipe(700)] #create an array of the pipes

    win = pygame.display.set_mode(screen_size) #create window to draw onto
    clock = pygame.time.Clock() #clock handles FPS

    run = True #game runs until it's true

    Iwannasee = 0
    while run:
        clock.tick(30) #FPS is 30
        Iwannasee +=1
        if Iwannasee == 100:
            run = False

        #draw everything
        draw_window(win, bird, pipes, base)


    pygame.quit() #quit
#end of main funciton


#calling main
if __name__ == "__main__":
    run_game()





