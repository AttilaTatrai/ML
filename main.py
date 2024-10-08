import pygame
import neat
#import time
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
        self.tick_count += 1

        delta = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if delta >= 16:
            delta = 16
        if delta < 0:
            delta -= 2

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
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
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
    VEL = 7
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    #setting up params
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

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

def draw_window(win, birds, pipes, base):
    win.blit(BG_IMG, (0,0)) #background drawing

    #draw all the pipes
    for pipe in pipes:
        pipe.draw(win)

    #show score
    pipe_passed = START_FONT.render("Score:  " + str(score), 1,(255, 255, 255))
    win.blit(pipe_passed, (5, 4))

    #shot generation
    generation_counter = START_FONT.render("Generation: " + str(generation),1,(255,255,255))
    win.blit(generation_counter, (5, 45))
    #show population
    genom_counter = START_FONT.render("Population: "
                                      + str(population)+"/"
                                      + str(len(birds)),1,(255,255,255))
    win.blit(genom_counter, (5, 90))

    base.draw(win)#ground drawing
    for bird in birds:
        bird.draw(win) #bird drawing

    pygame.display.update() #screen updtaing
#end of draw_window function


def object_mover(win, birds, pipes, base, gen, nets):
    trash = [] #pipe trash
    global score
    global FPS

    #we have to know wich pipe is in front of the birds
    #so we can make dicision to jump or not
    pipe_ind = 0
    if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
    else:
        return False

    #check the birds
    for count, bird in enumerate(birds):
        bird.move() #change pos of birds(down) ai will make it jump
        gen[count].fitness += 0.1 #increase a little bit the fitness

        #AI will make decision knowing these data
        data_to_evaluate = (bird.y,
                            abs(bird.y - pipes[pipe_ind].height),
                            abs(bird.y - pipes[pipe_ind].bottom))

        #let's make a decision without human intervention
        result = nets[count].activate(data_to_evaluate)

        #result is between 0 and 1 (sigmoid activation function)
        if result[0] > 0.5: #if pretty sure
            bird.jump()
    #bird cheker loop is over

    #manage pipes
    for pipe in pipes:
        pipe.move() #change the position of pipes

        #check pipe - bird collision
        for count, bird in enumerate(birds):
            if pipe.collide(bird):
                gen[count].fitness -= 1 #decrease fitness
                birds.remove(bird) #delete bird
                nets.pop(count) #delete
                gen.pop(count) #delete

            #bird left the pipe sucessfuly
            if pipe.passed == False and pipe.x < bird.x:
                pipe.passed = True
                score += 1 #increase score

                for g in gen:
                    g.fitness += 5 #increase fitness
                pipes.append(Pipe(WIN_WIDTH+100)) #add another pipe
    #end of bird and pipe loops

        #check if pipe left the window
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            trash.append(pipe)

        #delete unseen pipes
    for r in trash:
        pipes.remove(r)
    #pipe management loop is over

    #check if any of the birds hit the gound, or fly away
    for count, bird in enumerate(birds):
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            gen[count].fitness -= 1 #decrease fitness
            birds.remove(bird)#delete bird
            nets.pop(count) #delete the brain (nn)
            gen.pop(count) #delete from generation
    #for loop is over

    base.move() #change position of the ground
    #above 10 pipes make it faster
    if score > 10 and FPS < 1000:
        FPS += 1
#end of object mover function

def run_game(genomes, config):

    #this runs for every new gen
    gen = []
    nets = []
    birds = []
    global generation
    global population

    generation += 1
    population = len(genomes)

    #setup every genomes (g) here
    #genome is a bird in the population
    for ID, g in genomes:
        #creating the neural network
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net) #nn's are colledted in this list
        birds.append(Bird(random.randrange(100,230),350)) #collecting the birds in list
        g.fitness = 0 # 0 exp
        gen.append(g) #collecting genoms in a list
    #genome setup is done

    pygame.init() #setting up the game engine
    pygame.display.set_caption("Super Birds 2024")

    base = Base(730) #creating the ground object
    pipes = [Pipe(700)] #create an array of the pipes

    win = pygame.display.set_mode(screen_size) #create window to draw onto
    clock = pygame.time.Clock() #clock handles FPS

    run = True #game runs until it's true
    while run:
        clock.tick(FPS) #FPS is 30

        #check the events, like click
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit pressed?
                run = False #stop running
                pygame.quit() #close game engine
                quit() #quit program
                break

        #lets move all objects
        if object_mover(win, birds, pipes, base, gen, nets) == False:
            run = False
            break

        #draw everything
        draw_window(win, birds, pipes, base)
    #end of while loop
#end of main funciton


def run( config_path ):

    try:
        #load the default parameters for neural networks
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config_path)
    except:
        print("error check the files")
        return

    #create a starter pop
    #pop consists of x birds (currently 100 by param file)
    population = neat.Population(config)

    #it excludes the main function for 50 times / 50 generations
    population.run(run_game, 50)

    #exit
    pygame.quit() #exit the game engine
    quit() #exit the program
#end of run function


#calling main
if __name__ == "__main__":
    #AI config file
    local_dir = os.path.dirname((__file__))
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    run(config_path)
