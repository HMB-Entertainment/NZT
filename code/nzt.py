import pygame, sys, os, itertools, random
from pygame.locals import *

pygame.init() 

# USER SETTINGS

SCALE = WINDOWWIDTH, WINDOWHEIGHT = 1920,1080 # enter WINDOWWIDTH and WINDOWHEIGHT for resolution
#SCALE = WINDOWWIDTH, WINDOWHEIGHT = 1020,580 # zack
TRIALS = 10 # number of trials
WAIT = 30 # wait time in seconds between images
LEVEL = 1 # match checks for image this number images back
THREEDEE = False # loads images from 3D directory
LIGHTNING = True # tracer mode to train visualization!
SLOW = 1 # At LEVEL = 2, 3 images per SLOW number of seconds.

# GLOBAL VARIABLES

INDEX = 0 # used for lightning
TRIALNUMBER = 0 # initially 0
ANSWER = -1 # no answer yet
BOLT = [] # lightning
EVENT3 = USEREVENT+3 # used for lightning
EVENT2 = USEREVENT+2 # for half-time tune
NEXTTRIAL = USEREVENT+1 # for waiting until next image
FPS = 30 # frames per second setting

# FUNCTIONS

def zeus(n, bolt): # lightning bolt generator 
    index = 1 # index, num, bolt are local variables
    num = 0
    while num < n:
        if index == len(bolt):
            index = 0
        yield bolt[index]
        index += 1
        num += 1

def getgame(game): # utility for getting int from game intlist
    return int(''.join(map(str,game)))
        
def play(x): # function for playing mp3
    path = os.path.join('sounds/mp3s', x) # finds mp3 x in dir
    pygame.mixer.music.load(path) # loads mp3
    pygame.mixer.music.play() # plays mp3
    
def next_trial(x, TRIALNUMBER, ANSWER, INDEX, BOLT): # function run at transition
    TRIALNUMBER += 1 # updates to indicate current trial
    if LIGHTNING and TRIALNUMBER < LEVEL: # lightning still growing
        pygame.time.set_timer(EVENT3, 1000*SLOW/(TRIALNUMBER + 1)) # next image in bolt
        INDEX = WAIT*(TRIALNUMBER + 1) - 1
        BOLT = list(zeus(INDEX, [getgame(game[i]) for i in range(TRIALNUMBER + 1)]))
    else: # lightning full size
        pygame.time.set_timer(EVENT3, 1000*SLOW/(LEVEL + 1)) # next image in bolt
        INDEX = WAIT*(LEVEL + 1) - 1
    	BOLT = list(zeus(INDEX, [getgame(game[i]) for i in range(TRIALNUMBER - LEVEL, TRIALNUMBER + 1)]))
    pygame.time.set_timer(EVENT2, WAIT*500) # sets timer for halftime warble
    trial_pic = images[getgame(game[TRIALNUMBER])]
    scaled_pic = pygame.transform.scale(trial_pic, SCALE) # gets surface for game
    DISPLAYSURF.blit(scaled_pic, (0,0)) # displays game
    if TRIALNUMBER > LEVEL: # you haven't seen enough images for your level to start playing
        if ANSWER == parse[TRIALNUMBER - LEVEL - 1]: # proceed
            play('right.mp3') # good job
        else:
            play('wrong.mp3') # :(
    return [TRIALNUMBER, ANSWER, INDEX, BOLT] # returns nothing

def stop_game(x, y, z, i, b): # quits game
    pygame.quit()
    sys.exit()

def event3(x, TRIALNUMBER, ANSWER, INDEX, BOLT): # function for lightning
    if INDEX == 1:
        pygame.time.set_timer(EVENT3, 0)
    scaled_pic = pygame.transform.scale(images[BOLT[0]], SCALE) # scale the image
    DISPLAYSURF.blit(scaled_pic, (0,0)) # display image
    BOLT = BOLT[1:]
    INDEX -= 1
    return [TRIALNUMBER, ANSWER, INDEX, BOLT] # return nothing
    
def event2(x, TRIALNUMBER, ANSWER, INDEX, BOLT): # function for halftime tune
    play('delta.mp3') # play tune
    pygame.time.set_timer(EVENT2, 0) # otherwise would interrupt right/wrong mp3
    return [TRIALNUMBER, ANSWER, INDEX, BOLT] # return nothing

def key_up(event, TRIALNUMBER, ANSWER, INDEX, BOLT): # function to for key tune and input
    [f, a] = events.get(event.key, ['',-1]) # get key and answer
    if (a != -1): # if key is asdfjkl;
        play(f) # play corresponding pitch
        ANSWER = a # mark user answer
    return [TRIALNUMBER, ANSWER, INDEX, BOLT] # return trial number and user answer

def nothing(a,b,c,d,e): return [b,c,d,e] # default

# LIST COMPREHENSIONS

cubeElem = list(itertools.product([1,2,3], [1,2,3], [1,2,3])) # coodinates as list
numCubeElem = [getgame(x) for x in cubeElem]  # coordinates as int
filenames = [os.path.join(['3D' if THREEDEE else '2D'][0], str(x) + '.png') for x in numCubeElem] # filepath
game = [cubeElem[random.randint(0,26)] for x in range(TRIALS + LEVEL)] # generates game per settings
parse = [sum([0 if abs(game[x][y] - game[x + LEVEL][y]) else 2**y for y in range(3)]) + 1 for x in range(TRIALS)] # right answers
images = dict(zip(numCubeElem,[pygame.image.load(i) for i in filenames])) # assoc list of surfaces with coordinate as key

events = dict(zip([K_a, K_s, K_d, K_f, K_j, K_k, K_l, K_SEMICOLON], # keypress identifiers as key
	 	  zip([str(x) + '.mp3' for x in range(1,9)], # (mp3, answer)
	    	      [1,7,6,4,5,3,2,8])))

main_switch = dict(zip([QUIT,NEXTTRIAL,EVENT2,EVENT3,KEYUP], # event type
		 [stop_game,next_trial,event2,event3,key_up])) # function

# INITIALIZE

fpsClock = pygame.time.Clock() # initiates pygame Clock object 
pygame.time.set_timer(USEREVENT+1, WAIT*1000) #timer for next image
pygame.time.set_timer(EVENT2, WAIT*500) #timer for delta.mp3 to warn user to input final answer

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) # initiates surface
DISPLAYSURF.blit(pygame.transform.scale(images[int(''.join(map(str, game[0])))], SCALE), (0,0)) # plays first image
pygame.display.set_caption('NZT - Version 0') # Alpha

# GAME LOOP

while True: 
    for event in pygame.event.get():
        if TRIALNUMBER == TRIALS + LEVEL -1:
             stop_game(0, 0, 0, 0, 0)
        f = main_switch.get(event.type, nothing)
        [TRIALNUMBER, ANSWER, INDEX, BOLT] = f(event, TRIALNUMBER, ANSWER, INDEX, BOLT)
    pygame.display.update()
    fpsClock.tick(FPS)
