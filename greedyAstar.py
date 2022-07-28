import numpy as np
import random
import sys

grid = np.zeros((1000,700),dtype=np.int16)
heuristicGrid = np.zeros((1000,700),dtype=np.int16)
def gridMaker():
    # grid = np.zeros((1000,700),dtype=np.int16)
    for xx in range(1000):
        for yy in range(700):
            grid[xx][yy] = 10

    # heuristicGrid = np.zeros((1000,700),dtype=np.int16)
    for xx in range(1000):
        for yy in range(700):
            heuristicGrid[xx][yy] = (xx + yy)



def makeSpecificGrid(x1,y1,x2,y2):
    # grid = np.zeros((1000,700),dtype=np.int16)
    # for xx in range(1000):
    #     for yy in range(700):
    #         grid[xx][yy] = 10
    # gridSize=1000
    # grids = [[10] * gridSize for _ in range(gridSize)]

    grid[x1][y1] = 1
    grid[x2][y2] = 0
    return grid

def aStarSearch(grid,x1,y1,x2,y2):
    grid[x1][y1] = 1
    grid[x2][y2] = 0
    # heuristicGrid = np.zeros((1000,700),dtype=np.int16)
    # for xx in range(1000):
    #     for yy in range(700):
    #         heuristicGrid[xx][yy] = (xx + yy)
    bestForPosition = np.zeros((1000,700),dtype=np.int16)
    currentlyActiveList = []
    currentPosition = (x2,y2)
    currentlyActiveList.append( (currentPosition,heuristicGrid[x2][y2]) ) # coordinates, a* value
    temp = 0
    
    ## find max values
    while currentlyActiveList and currentPosition!=(x1,y1):
        temp += 1
        currentlyActiveList = \
            [(coords, score) for (coords, score) in currentlyActiveList if coords != currentPosition]

        #for x
        if currentPosition[0]>x1:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition1x][possPosition1y] \
                +heuristicGrid[possPosition1x][possPosition1y]
            currentlyActiveList.append( ((possPosition1x, possPosition1y), aStarScore1))
            bestForPosition[possPosition1x][possPosition1y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                     + grid[possPosition1x][possPosition1y],\
                 bestForPosition[possPosition1x][possPosition1y])

        elif currentPosition[0]<x1:
            possPosition1x = currentPosition[0]+1
            possPosition1y = currentPosition[1]
            
            aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition1x][possPosition1y] \
                +heuristicGrid[possPosition1x][possPosition1y]
            currentlyActiveList.append( ((possPosition1x, possPosition1y), aStarScore1))
            bestForPosition[possPosition1x][possPosition1y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                     + grid[possPosition1x][possPosition1y],\
                 bestForPosition[possPosition1x][possPosition1y])

#         print(possPosition2x)

        #for y
        if currentPosition[1]>y1:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition2x][possPosition2y] \
                +heuristicGrid[possPosition2x][possPosition2y]
            currentlyActiveList.append( ((possPosition2x, possPosition2y), aStarScore2))
            bestForPosition[possPosition2x][possPosition2y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                     + grid[possPosition2x][possPosition2y],\
                 bestForPosition[possPosition2x][possPosition2y])
            
        elif currentPosition[1]<y1:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]+1
            aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition2x][possPosition2y] \
                +heuristicGrid[possPosition2x][possPosition2y]
            currentlyActiveList.append( ((possPosition2x, possPosition2y), aStarScore2))
            bestForPosition[possPosition2x][possPosition2y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                     + grid[possPosition2x][possPosition2y],\
                 bestForPosition[possPosition2x][possPosition2y])

        sorted_by_second = currentlyActiveList.sort(key=lambda tuple: tuple[1], reverse=True)
        #print("currently active: ",currentlyActiveList)
        if not currentlyActiveList:
            break
        currentPosition = currentlyActiveList[0][0]
#         print(currentPosition)
        #print(grid)
        #print(bestForPosition)
        #input()
    ## construct best path
    #print(bestForPosition)
    pathGrid = np.zeros( (1000,700), dtype=np.int16) #just for illustration
    path = []
    currentPosition = (x2,y2)
    path.append( (x2,y2) )
    pathGrid[x2][y2] = True
    while currentPosition != (x1,y1):
        pos1=False
        pos2=False
        possPosition1x=currentPosition[0]
        possPosition1y=currentPosition[1]
        possPosition2x=currentPosition[0]
        possPosition2y=currentPosition[1]
#         print(currentPosition)
        if currentPosition[0]>x1:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            pos1 = True
        elif currentPosition[0]<x1:
            possPosition1x = currentPosition[0]+1
            possPosition1y = currentPosition[1]
            pos1 = True
        if currentPosition[1]>y1:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            pos2 = True
        elif currentPosition[1]<y1:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]+1
            pos2 = True
        pos1Bigger = bestForPosition[possPosition1x][possPosition1y]>\
            bestForPosition[possPosition2x][possPosition2y]
        if (pos1 and not pos2) or (pos1 and pos2 and pos1Bigger):
            path.append( (possPosition1x,possPosition1y) )
            pathGrid[possPosition1x][possPosition1y] = 1
            currentPosition = (possPosition1x,possPosition1y)
        if (pos2 and not pos1) or (pos1 and pos2 and not pos1Bigger):
            path.append( (possPosition2x,possPosition2y) )
            pathGrid[possPosition2x][possPosition2y] = 1
            currentPosition = (possPosition2x,possPosition2y)
    # print(grid)
    # print(path)
    # print(pathGrid)
    grid[x1][y1] = 10
    grid[x2][y2] = 10
    path.reverse()
    return(path)

# aStarSearch(makeSpecificGrid(makeSpecificGrid(x1,y1,x2,y2),x1,y1,x2,y2))
# aStarSearch(makeSpecificGrid(444,999,99,79),444,999,99,79)