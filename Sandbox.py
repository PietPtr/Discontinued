import pygame, sys, time, random
from pygame.locals import *

# -------- Image and music Loading --------

stoneImg = pygame.transform.scale(pygame.image.load('stone.png'), (50, 50))
stoneeImg = pygame.transform.scale(pygame.image.load('stonee.png'), (50, 50))
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
            #"""
            if y >= 10:
                world[y][x] = Stone([x, y], 0)
            elif y < 10:
                world[y][x] = Air([x, y], 0)
            """
            if random.randint(0,1) == 0:
                world[y][x] = Stone([x, y], 0)
            else:
                world[y][x] = Air([x, y], 0)
            """
            

def checkCollision(tile):
    locked = False
    pygame.draw.rect(windowSurface, RED, tile.rect, 1)
    try:
        if world[tile.position[1] + 1][tile.position[0]].type != "Air": #Down
            print "True1"
            locked = True
    except:
        print "OutOfRange@1"
    try:
        if world[tile.position[1]][tile.position[0] + 1].type != "Air": #Right
            print "True2"
            locked = True
    except:
        print "OutOfRange@2"
    if world[tile.position[1]][tile.position[0] - 1].type != "Air" and tile.position[0] - 1 >= 0: #Left
        print "True3"
        locked = True
    if world[tile.position[1] - 1][tile.position[0]].type != "Air" and tile.position[1] - 1 >= 0: #Up
        print "True4"
        locked = True
    if locked == False:
        world[tile.position[1]][tile.position[0]] = Air([tile.position[0], tile.position[1]], 0)
        entityList.append(Entity([tile.position[0] * 50, tile.position[1] * 50], stoneeImg, [0, 0.1]))
    elif locked == True:
        world[mousePosition[1]][mousePosition[0]] = Stone([mousePosition[0], mousePosition[1]], 0.1)

def turnIntoEntity(tile):
    pass    

class Block(object):
    global frameTime
    def __init__(self, position, speed, texture):
        self.position = position    # X * 50 = displayX, Y * 50  = displayY
        self.speed = speed
        self.rect = pygame.Rect(position[0] * 50, position[1] * 50, 50, 50)
        self.locked = False
    def render(self):
        windowSurface.blit(self.texture, (self.position[0] * 50, self.position[1] * 50))
        

class Stone(Block):
    def __init__(self, position, speed):
        self.texture = stoneImg
        Block.__init__(self, position, speed, self.texture)
        self.type = "Stone"
    
class Air(Block): #or grid
    def __init__(self, position, speed):
        self.texture = airImg
        Block.__init__(self, position, speed, self.texture)
        self.type = "Air"

class Entity(object):
    def __init__(self, position, texture, movement):
        self.position = position    # Real on screen position
        self.texture =  texture
        self.movement = movement
    def render(self):
        windowSurface.blit(self.texture, (self.position[0], self.position[1]))
        self.position[0] = self.position[0] + self.movement[0]
        self.position[1] = self.position[1] + self.movement[1]

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

mousePosition = [0,0]

showDebug = True
clicked = False

world = []

entityList = []

# -------- Objects --------
for i in range(0, WINDOWHEIGHT / 50):
    world.append([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])

generateWorld()

loopTrack = 0
while True:
    # -------- Update loop specific variable --------
    loopTrack = loopTrack + 1
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePos = pygame.mouse.get_pos()
    mousePosition[0] = (mousePos[0] - (mousePos[0] % 50)) / 50
    mousePosition[1] = (mousePos[1] - (mousePos[1] % 50)) / 50

    # -------- Code outside Gamestate --------
    windowSurface.blit(background, (0, 0))
    
    # -------- Gameplay --------

    windowSurface.blit(transStone, (mousePos[0] - (mousePos[0] % 50), mousePos[1] - (mousePos[1] % 50)))

    if clicked == True:
        #world[mousePosition[1]][mousePosition[0]] = Stone([mousePosition[0], mousePosition[1]], 0.1)
        checkCollision(world[mousePosition[1]][mousePosition[0]])
    
    for y in range(0,14):
        for x in range(0,26):
            try:
                world[y][x].render()
            except AttributeError:
                print "AttributeError"

            

    for entity in entityList:
        entity.render()
    
    # -------- Debugging --------
    if showDebug == True:
        debug = int(FPS)
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # -------- Events --------
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            clicked = True
        elif event.type != MOUSEBUTTONUP:
            clicked = False
        if event.type == KEYUP and event.key == 284:
            showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
