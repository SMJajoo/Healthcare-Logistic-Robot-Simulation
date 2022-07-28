import numpy as np
import random
import sys
import math

def makeSpecificGrid(x1,y1,x2,y2):
    grid = np.zeros((1000,700),dtype=np.int16)
    # for xx in range(max(0,min(x1,x2)-3),min(max(x1,x2)+3,1000)):
    #     for yy in range(max(0,min(y1,y2)-3),min(max(y1,y2)+3,1000)):
    for xx in range(1000):
        for yy in range(700):
            grid[xx][yy] = math.sqrt( (xx-x2)*(xx-x2) + (yy-y2)*(yy-y2) )
    # print(grid)
    return grid


def aStarSearch(grid,x1,y1,x2,y2):
    currentPosition=(x1,y1)
    endPosition=(x2,y2)
    bestPath=[]
    while currentPosition!=endPosition:
        bestPosition=checkNeighbors(currentPosition,grid)[0]
        bestPath.append(bestPosition)
        currentPosition=bestPosition
    return bestPath

def neighbours(current):
    neighbours = []
    x = current[0]
    y = current[1]
    for a in range(x - 1, x + 2):
        if a < 0 or a > 1000:
            continue
        for b in range(y - 1, y + 2):
            if b < 0 or b > 700:
                continue
            neighbours.append((a,b))
    neighbours.remove((x,y))
    return neighbours        
        
def checkNeighbors(current,grid):
    bestPosition=(current,grid[current[0]][current[1]])
    min_value=0
    for i in neighbours(current):
        score=grid[i[0]][i[1]]
        if score < bestPosition[1]:
            bestPosition=((i[0],i[1]),score)
    return bestPosition






