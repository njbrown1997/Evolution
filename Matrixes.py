import random, time
import numpy

def createRandomBinaryMatrix(m,n,z):
    matrix = numpy.zeros((n,m))
    matrix[int(n/2)][int(m/2)] = -1
    insertedOnes = 0
    while insertedOnes < z:
        row = random.randint(0,n-1)
        col = random.randint(0,m-1)
        if matrix[row][col] == 0:
            matrix[row][col] = 1
            insertedOnes += 1
    return matrix
