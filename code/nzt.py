import pygame, sys, os, random
from pygame.locals import *

pygame.init() # initiate pygame

# USER ADJUSTABLE SETTINGS

WINDOWWIDTH = 1920 # width in pixels
WINDOWHEIGHT = 1080 # height in pixels
#WINDOWWIDTH = 1020 # width in pixels
#WINDOWHEIGHT = 580 # height in pixels
TRIALS = 10 # number of trials
WAIT = 30 # wait time in seconds between images
LEVEL = 1 # match checks for image this number images back
THREEDEE = False # loads images from 3D directory

# END OF USER ADJUSTABLE SETTINGS

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock() # initiates pygame Clock object 

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) # initiates surface
pygame.display.set_caption('NZT - Version 0') # Higgs Edition 

cubeElem = [[x,y,z] for x in [1,2,3] for y in [1,2,3] for z in [1,2,3]] # list of list of all elems
charCubeElem = [[str(y) for y in x] for x in cubeElem] # list of all elements as list of chars
strCubeElem = [''.join(x) for x in charCubeElem] # should I map this and combine comprehensions?
numCubeElem = [int(x) for x in strCubeElem]  # {xyz | x,y,z in Z AND 0 < x,y,z < 4} 
filenames3D = [os.path.join("3D", str(x)+'.png') for x in strCubeElem] # convert to files for ease of loading
filenames2D = [os.path.join("2D", (str(x)+'.png')) for x in strCubeElem] # convert to files for ease of loading

if THREEDEE == False:
    filenames = filenames2D
else:
    filenames = filenames3D

images = dict(zip(numCubeElem, [pygame.image.load(i) for i in filenames])) #create associative array for images
# sounds = dict(zip(['K_'+str(x) for x in range(1,9)], [str(x)+'.mp3' for x in range(1,9)]))
# running a for loop over the dictionary doesn't let me play mp3s.

def lstdiff(lst1, lst2): # useful for finding which x,y, or z same or different
    return [0 if abs(lst1[i] - lst2[i]) else 1 for i in range(3)]

def lstpts(lsd): # assigns 1,2,4 points for x,y,z so each possible answer has a unique number
    return sum(lsd[i]*(2**i) for i in range(3))

def play(x):
    path = os.path.join('sounds/mp3s', x)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
events = {K_a: ['1.mp3', 1],
          K_s: ['2.mp3', 7],
          K_d: ['3.mp3', 6],
          K_f: ['4.mp3', 4],
          K_j: ['5.mp3', 5],
          K_k: ['6.mp3', 3],
          K_l: ['7.mp3', 2],
          K_SEMICOLON: ['8.mp3', 8]}
def key_up(Key):
    [f, a] = events[Key]
    play(f)
    answer = a

game = [cubeElem[random.randint(0,26)] for i in range(TRIALS + LEVEL)] #generates game according to user settings
parse = [lstpts(lstdiff(game[i],game[i+LEVEL]))+1 for i in range(TRIALS)] #generates game answers

DISPLAYSURF.blit(pygame.transform.scale(images[int(''.join(map(str,game[0])))], (WINDOWWIDTH, WINDOWHEIGHT)), (0,0)) # plays first image
pygame.time.set_timer(USEREVENT+1, WAIT*1000) #timer for next image
pygame.time.set_timer(USEREVENT+2, WAIT*500) #timer for delta.mp3 to warn user to input final answer

trialnumber = 0
answer = -1

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT or trialnumber == TRIALS + LEVEL -1:
            pygame.quit()
            sys.exit()
        if event.type == USEREVENT+2:
            play('delta.mp3')
            pygame.time.set_timer(USEREVENT+2, 0)
        if event.type == USEREVENT+1:
            pygame.time.set_timer(USEREVENT+2, WAIT*500)
            trialnumber += 1
            DISPLAYSURF.blit(pygame.transform.scale(images[int(''.join(map(str,game[trialnumber])))], (WINDOWWIDTH, WINDOWHEIGHT)), (0,0))
            if trialnumber > LEVEL:
                if answer == parse[trialnumber-LEVEL-1]:
                    play('right.mp3')
                else:
                    play('wrong.mp3')
        if event.type == KEYUP:
            key_up(event.key)
    pygame.display.update()
    fpsClock.tick(FPS)

