#Imports
from venv import create
import pygame, sys
from pygame.locals import *
import random, time
import numpy
from Matrixes import *
from Monkey import *
import pickle

STEP_TIME = .5

def simulate(M,worldMatrix,moveCapacity, manualControl, render):
    ROWS,COLS = worldMatrix.shape
    M.coords = (int(ROWS/2),int(COLS/2))
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
            if M.moveAI(worldMatrix) and render:
                 time.sleep(STEP_TIME)

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

def Battle(C1,C2,trials):
    score1 = 0
    score2 = 0

    for i in range(0,trials):
        worldMatrix= createRandomBinaryMatrix(9,7,25)
        worldMatrixCopy = worldMatrix.copy()
        simulate(C1,worldMatrix,50,False, False)
        score1 += C1.foodEaten
        C1.foodEaten = 0
        simulate(C2,worldMatrixCopy,50,False, False)
        score2 += C2.foodEaten
        C2.foodEaten = 0

    return score1/trials, score2/trials


def HillClimb(generations,trials,seedFileName,fileName):
    B = pickle.load(open(seedFileName +".pickle","rb"))
    C1 = Chimp(9)
    C1.brain = numpy.copy(B)
    finalFitness = 0
    for i in range(0,generations):
        C2 = Chimp(9)
        C2.brain = numpy.copy(C1.brain)
        C2.mutateExp()

        fitness = Battle(C1,C2,trials)
        print(fitness)
        finalFitness = fitness[0]
        if fitness[1] > fitness [0]:
            C1.brain = numpy.copy(C2.brain)
            finalFitness = fitness[1]

    pickle.dump(C1.brain,open(fileName + str(finalFitness) + ".pickle","wb"))
    return fileName + str(finalFitness)

def ObserveMonkey(fileName):
    B = pickle.load(open(fileName +".pickle","rb"))
    C = Chimp(9)
    C.brain = numpy.copy(B)
    print(C.brain)
    worldMatrix = createRandomBinaryMatrix(9,7,25)
    simulate(C,worldMatrix,50,False,True)

def Evolve(generations,trials,seedFileName,fileName):
    resultMonkeyFile = HillClimb(generations,trials,seedFileName,fileName)
    ObserveMonkey(resultMonkeyFile)

for i in range(0,10):
    ObserveMonkey("monkey14-117")                                                                                                                                  