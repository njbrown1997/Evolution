#Imports
from venv import create
import pygame, sys
from pygame.locals import *
import random, time
import numpy
from Matrixes import *


TILE_SIZE = 100

class Food(pygame.sprite.Sprite):
      def __init__(self,x,y):
        super().__init__() 
        self.image = pygame.transform.scale(pygame.image.load("Banana.png"),(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (y*TILE_SIZE + TILE_SIZE/2,x*TILE_SIZE + TILE_SIZE/2)
 
class Monkey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(pygame.image.load("Monkey.png"),(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect()
        self.coords = (0,0)
        self.rect.center = (TILE_SIZE/2,TILE_SIZE/2)
        self.movesMade = 0
        self.foodEaten = 0

    def updateLocation(self,worldMatrix,x,y):
        ROWS,COLS = worldMatrix.shape
        if 0 <= x < ROWS and 0 <= y < COLS and (x != self.coords[0] or y != self.coords[1]):
            worldMatrix[self.coords[0]][self.coords[1]] = 0
            if worldMatrix[x][y] == 1:
                self.foodEaten += 1
            self.coords = (x,y)
            worldMatrix[x][y] = -1
            self.rect.center = (y*TILE_SIZE + TILE_SIZE/2,x*TILE_SIZE + TILE_SIZE/2)
            self.movesMade += 1
            return True
        else:
            return False

    def moveAI(self,worldMatrix):
        num = random.randint(1,4)
        if num == 1:
                if self.updateLocation(worldMatrix,self.coords[0] + 1,self.coords[1]):
                    return True
        elif num == 2:
                if self.updateLocation(worldMatrix,self.coords[0] - 1,self.coords[1]):
                    return True
        elif num == 3:
                if self.updateLocation(worldMatrix,self.coords[0],self.coords[1]+1):
                    return True
        else:
                if self.updateLocation(worldMatrix,self.coords[0] ,self.coords[1]-1):
                    return True
        return False

def simulate(M,worldMatrix,moveCapacity, manualControl, render):
    ROWS,COLS = worldMatrix.shape
    if render:
        #Initializing 
        pygame.init()

        #Setting up FPS 
        FPS = 60
        FramePerSec = pygame.time.Clock()
        
        #Creating colors
        BLUEGRAY = (40,40,80)
        
        #Create a white screen 
        DISPLAYSURF = pygame.display.set_mode((TILE_SIZE*COLS,TILE_SIZE*ROWS))
        DISPLAYSURF.fill(BLUEGRAY)
        pygame.display.set_caption("Evolution")

        #Creating Sprites Groups
        food = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        #Setting up Sprites        
        for i in range(0, ROWS):
            for j in range(0,COLS):
                if worldMatrix[i,j] == 1:
                    F = Food(i,j)
                    food.add(F)
                    all_sprites.add(F)
                elif worldMatrix[i,j] == -1:
                    M.updateLocation(worldMatrix,i,j)
                    all_sprites.add(M)
    else:
        for i in range(0, ROWS):
            for j in range(0,COLS):
                if worldMatrix[i,j] == -1:
                    M.updateLocation(worldMatrix,i,j)

    M.movesMade = M.foodEaten = 0
    #Game Loop
    while M.movesMade < moveCapacity:
        if render:
            pygame.display.set_caption("Moves Made: " + str(M.movesMade) + " | Food Eaten: " + str(M.foodEaten))
            DISPLAYSURF.fill(BLUEGRAY)
            #Moves and Re-draws all Sprites
            for entity in all_sprites:
                DISPLAYSURF.blit(entity.image, entity.rect)

            pygame.display.update()
            #Cycles through all events occuring  
            for event in pygame.event.get():           
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if manualControl:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            M.updateLocation(worldMatrix,M.coords[0] + 1,M.coords[1])
                        if event.key == pygame.K_UP:
                            M.updateLocation(worldMatrix,M.coords[0] - 1,M.coords[1])
                        if event.key == pygame.K_RIGHT:
                            M.updateLocation(worldMatrix,M.coords[0],M.coords[1]+1)
                        if event.key == pygame.K_LEFT:
                            M.updateLocation(worldMatrix,M.coords[0] ,M.coords[1]-1)
                    
        if not(manualControl) or not(render):
            if M.moveAI(worldMatrix) and render: time.sleep(.1)

        if render:
            #To be run if collision occurs between Monkey and Food
            collision = pygame.sprite.spritecollideany(M, food)
            if collision:
                pygame.display.update()
                collision.kill()

    #End Screen
    if render:
        pygame.display.set_caption("Moves Made: " + str(M.movesMade) + " | Food Eaten: " + str(M.foodEaten))
        DISPLAYSURF.fill(BLUEGRAY)
        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
        pygame.display.update()
        #To be run if collision occurs between Monkey and Food
        collision = pygame.sprite.spritecollideany(M, food)
        if collision:
            pygame.display.update()
            collision.kill()
        time.sleep(2)


##################################################################################
###########################    Run Simulations    ################################
##################################################################################

worldMatrix= createRandomBinaryMatrix(9,7,30)
M = Monkey()
simulate(M,worldMatrix,50,False, True)
print(M.foodEaten)

worldMatrix= createRandomBinaryMatrix(9,7,30)
simulate(M,worldMatrix,50,False, False)
print(M.foodEaten)

worldMatrix= createRandomBinaryMatrix(9,7,1)
simulate(M,worldMatrix,50,False, True)
print(M.foodEaten)