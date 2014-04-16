import pygame, sys
from pygame.locals import *

# -------- Image and music Loading --------

stoneImg = pygame.transform.scale(pygame.image.load('stone.png'), (50, 50))
transStone = pygame.transform.scale(pygame.image.load('stone.png'), (50, 50))
transStone.set_alpha(150)
airImg = pygame.transform.scale(pygame.image.load('grid.png'), (50, 50))

background = pygame.image.load('bg.png')

# -------- Classes and Functions --------

def restart():
    pass

def distance(speed, time):
    distance = time * speed
    return distance

def generateWorld():
    for y in range(0,14):
        for x in range(0,26):
            if y >= 10:
                world[y][x] = Stone([x, y], 0)
            elif y < 10:
                world[y][x] = Air([x, y], 0)

class Block(object):
    def __init__(self, position, speed, texture):
        self.position = position    # X * 50 = displayX, Y * 50  = displayY
        self.speed = speed
    def render(self):
        windowSurface.blit(self.texture, (self.position[0] * 50, self.position[1] * 50))

class Stone(Block):
    def __init__(self, position, speed):
        self.texture = stoneImg
        Block.__init__(self, position, speed, self.texture)
    
class Air(Block): #or grid
    def __init__(self, position, speed):
        self.texture = airImg
        Block.__init__(self, position, speed, self.texture)


# -------- Constants --------

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 200, 0)

WINDOWWIDTH = 1300
WINDOWHEIGHT = 700

# -------- Set up --------

pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Sandbox')
basicFont = pygame.font.SysFont(None, 23)
mainClock = pygame.time.Clock()

# -------- Other variables --------

showDebug = True

world = []

for i in range(0, WINDOWHEIGHT / 50):
    world.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])

generateWorld()

# -------- Objects --------

loopTrack = 0
while True:
    # -------- Update loop specific variable --------
    loopTrack = loopTrack + 1
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePos = pygame.mouse.get_pos()

    # -------- Code outside Gamestate --------
    windowSurface.blit(background, (0, 0))
    
    # -------- Gameplay --------

    windowSurface.blit(transStone, (mousePos[0] - (mousePos[0] % 50), mousePos[1] - (mousePos[1] % 50)))

    
    for y in range(0,14):
        for x in range(0,26):
            try:
                world[y][x].render()
            except AttributeError:
                print AttributeError
    
    # -------- Debugging --------
    if showDebug == True:
        debug = int(FPS)
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # -------- Events --------
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == 284:
            showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
