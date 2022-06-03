#Imports
from turtle import shape
from venv import create
import pygame, sys
from pygame.locals import *
import random, time
import numpy
from Matrixes import *
import math

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
            self.movesMade += 1
            return True 
        
            #return False

    def moveRandom(self,worldMatrix):
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
    
    def moveAI(self,worldMatrix):
        return self.moveRandom(worldMatrix)

class FibMonkey(Monkey):
    def __init__(self):
        super().__init__() 
        self.p1 = 1
        self.p2 = 0

    def moveAI(self,worldMatrix):
        temp = self.p1 + self.p2
        self.p1 = self.p2
        self.p2 = temp
        num = temp % 4

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

class Chimp(Monkey):
    def __init__(self,COLS):
        super().__init__() 
        self.brain = numpy.random.rand(COLS,COLS)

    def moveAI(self,worldMatrix):
        ROWS,COLS = worldMatrix.shape
        result = numpy.matmul(worldMatrix,self.brain)

        if self.coords[0] + 1 < ROWS:
            down = result[self.coords[0] + 1][self.coords[1]]
        else:
            down = 0

        if self.coords[0] - 1 >= 0:
            up = result[self.coords[0] - 1][self.coords[1]]
        else:
            up = 0

        if self.coords[1] - 1 >= 0:
            left = result[self.coords[0]][self.coords[1]-1]
        else:
            left = 0

        if self.coords[1] + 1 < COLS:
            right = result[self.coords[0]][self.coords[1]+1]
        else:
            right = 0

        num = max(up,left,right,down)

        if num == down:
                if self.updateLocation(worldMatrix,self.coords[0] + 1,self.coords[1]):
                    return True
        elif num == up:
                if self.updateLocation(worldMatrix,self.coords[0] - 1,self.coords[1]):
                    return True
        elif num == right:
                if self.updateLocation(worldMatrix,self.coords[0],self.coords[1]+1):
                    return True
        else:
                if self.updateLocation(worldMatrix,self.coords[0] ,self.coords[1]-1):
                    return True
        return False

    def mutate(self):
        i = random.randint(0,self.brain.shape[0]-1)
        j = random.randint(0,self.brain.shape[0]-1)
        self.brain[i][j] = random.random()
        #scale = 1 + (random.random() - 1/2)/8
        #self.brain[i][j] = self.brain[i][j]*scale
