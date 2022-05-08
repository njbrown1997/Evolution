#Imports
from venv import create
import pygame, sys
from pygame.locals import *
import random, time
import numpy
from Matrixes import *
 
#Initializing 
pygame.init()

MANUAL = False

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUEGRAY = (40,40,80)
 
#Other Variables for use in the program
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SPEED = 5
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLUEGRAY)
pygame.display.set_caption("Evolution")
 
worldMatrix = createRandomBinaryMatrix(int(SCREEN_WIDTH/100),int(SCREEN_HEIGHT/100),10)
numRows, numCols = worldMatrix.shape

class Food(pygame.sprite.Sprite):
      def __init__(self,x,y):
        super().__init__() 
        self.image = pygame.image.load("Banana.png")
        self.rect = self.image.get_rect()
        self.coords = (x,y)
        self.rect.center = (y*100 +50,x*100 + 50)
 
class Monkey(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image = pygame.image.load("Monkey.png")
        self.rect = self.image.get_rect()
        self.coords = (x,y)
        self.rect.center = (y*100 +50,x*100 + 50)
        self.movesMade = 0
        self.foodEaten = 0

    def updateLocation(self,x,y):
        if 0 <= x < numRows and 0 <= y < numCols and (x != self.coords[0] or y != self.coords[1]):
            worldMatrix[self.coords[0]][self.coords[1]] = 0
            self.coords = (x,y)
            worldMatrix[x][y] = -1
            self.rect.center = (y*100 +50,x*100 + 50)
            self.movesMade += 1

    def moveAI(self):
        time.sleep(.5)
        num = random.randint(1,4)
        if num == 1:
                M.updateLocation(M.coords[0] + 1,M.coords[1])
        elif num == 2:
                M.updateLocation(M.coords[0] - 1,M.coords[1])
        elif num == 3:
                M.updateLocation(M.coords[0],M.coords[1]+1)
        else:
                M.updateLocation(M.coords[0] ,M.coords[1]-1)


#Creating Sprites Groups
food = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#Setting up Sprites        
for i in range(0, numRows):
    for j in range(0,numCols):
        if worldMatrix[i,j] == 1:
            F = Food(i,j)
            food.add(F)
            all_sprites.add(F)
        elif worldMatrix[i,j] == -1:
            M = Monkey(i,j)
            all_sprites.add(M)

  
#Game Loop
while M.movesMade < 50:
    pygame.display.set_caption("Moves Made: " + str(M.movesMade) + " | Food Eaten: " + str(M.foodEaten))
    #Cycles through all events occuring  
    for event in pygame.event.get():           
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if MANUAL:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    M.updateLocation(M.coords[0] + 1,M.coords[1])
                if event.key == pygame.K_UP:
                    M.updateLocation(M.coords[0] - 1,M.coords[1])
                if event.key == pygame.K_RIGHT:
                    M.updateLocation(M.coords[0],M.coords[1]+1)
                if event.key == pygame.K_LEFT:
                    M.updateLocation(M.coords[0] ,M.coords[1]-1)
                
    DISPLAYSURF.fill(BLUEGRAY)
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
    if not(MANUAL):
         M.moveAI()
    
    #To be run if collision occurs between Monkey and Food
    collision = pygame.sprite.spritecollideany(M, food)
    if collision:
          pygame.display.update()
          worldMatrix[collision.coords[0]][collision.coords[1]] = -1
          collision.kill()
          M.foodEaten += 1
         
    pygame.display.update()
    FramePerSec.tick(FPS)