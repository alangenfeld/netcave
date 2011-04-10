# -*- coding: utf-8 -*-
import random, numpy

def cellDungeon(width=50,height=50,rand=.55,seed=random.randint(100000,100000000),first=4,second=3,n=2,c=2):

    dungeon = numpy.ones((height,width),dtype=numpy.uint)
    
    for x in range(1,width-1):
        for y in range(1,height-1):
            if random.random()<rand:
                dungeon[y,x] = 0

    for x in range(0,first):
        dungeon = fiveFourSpace(dungeon,n,c)

    for x in range(0,second):
        dungeon = fiveFour(dungeon)

    return dungeon


def fiveFour(dungeon):
    height,width = dungeon.shape
    nextD = numpy.zeros((height,width),dtype=numpy.uint)  

    for x in range(0,width):
        for y in range(0,height):
            if cellCount(dungeon,x,y) >= 5:
                nextD[y,x] = 1

    return nextD

def fiveFourSpace(dungeon,n=2,c=2):
    height,width = dungeon.shape
    nextD = numpy.zeros((height,width),dtype=numpy.uint)  

    for x in range(0,width):
        for y in range(0,height):
            if cellCount(dungeon,x,y) >= 5 or cellCount(dungeon,x,y,n=2) <= c:
                nextD[y,x] = 1

    return nextD


def cellCount(dungeon,x,y,n=1):
    height,width = dungeon.shape
    count=0

    for j in range(x-n,x+n+1):
        for k in range(y-n,y+n+1):
            if j<0 or k<0 or j>width-1 or k>height-1:
                count+=1
            elif dungeon[k,j] == 1:
                count+=1
    return count

def firstZero(dungeon):
    height,width = dungeon.shape

    for x in range(0,width):
        for y in range(0,height):
            if dungeon[y,x]==0:
                return (x,y)

    return (-1,-1)

def floodFill(dungeon,x,y,diag=True, search=0,replace=1):

    height,width = dungeon.shape

    if x<0 or y<0 or x>=width or y>=height or not(dungeon[y,x] == search):
        return

    dungeon[y,x]=replace

    if diag:
        for j in range(x-1,x+2):
            for k in range(y-1,y+2):
                if j==x and k==y:
                    pass
                else:
                    floodFill(dungeon,j,k,diag,search,replace)
    else:
        floodFill(dungeon,x-1,y,diag,search,replace)
        floodFill(dungeon,x+1,y,diag,search,replace)
        floodFill(dungeon,x,y-1,diag,search,replace)
        floodFill(dungeon,x,y+1,diag,search,replace)
            
    

def connected(dungeon,diag=True):
    height,width = dungeon.shape

    j,k = firstZero(dungeon)

    if j==-1:
        return False

    d2 = numpy.array(dungeon,copy=False)
    floodFill(d2,j,k,diag)

    j,k = firstZero(dungeon)

    if k == -1:
        return True

    return False

def connected2(dungeon):
    d2 = numpy.array(dungeon)
    height,width = dungeon.shape
    for x in range(0,width):
        for y in range(0,height):
            if d2[y,x]==2:
                d2[y,x]=1
            elif d2[y,x]>2:
                d2[y,x]=0
    return connected(d2,False)

def printDungeon(dungeon):
    
    height,width = dungeon.shape
    for y in range(0,height):
        s = ''
        for x in range(0,width):
            if dungeon[y,x]==0:
                s+=' '
            elif dungeon[y,x]==2:
                s+="#"
            elif dungeon[y,x]==3:
                s+='['
            elif dungeon[y,x]==4:
                s+='D'
            elif dungeon[y,x]==5:
                s+='T'
            elif dungeon[y,x]==6:
                s+='#'
            elif dungeon[y,x]==7:
                s+="<"
            elif dungeon[y,x]==8:
                s+=">"
            elif dungeon[y,x]==9:
                s+="S"
            else:
                s+='#'
        print(s)

def trimDungeon(dungeon):
    height,width = dungeon.shape
    minX,minY,maxX,maxY = (0,0,0,0)

    #print width
    #print height

    for x in range(1,width-1):
        for y in range(1,height-1):
            if dungeon[y,x] == 0:
                minX = x
                x=width
                break
        if x==width:
            break
    for y in range(1,height-1):
        for x in range(1,width-1): 
            if dungeon[y,x] == 0:
                minY = y
                y=height
                break
        if y==height:
            break

    for x in range(width-2,1,-1):
        for y in range(height-2,1,-1):
            if dungeon[y,x] == 0:
                maxX = x
                x=0
                break
        if x==0:
            break
    for y in range(height-2,1,-1):
        for x in range(width-2,1,-1): 
            if dungeon[y,x] == 0:
                maxY = y
                y=0
                break
        if y==0:
            break

    #print (minX,minY,maxX,maxY)

    return numpy.array(dungeon[minY-1:maxY+2,minX-1:maxX+2])

def getRoom(width=50,height=50,rand=.55,seed=random.randint(100000,100000000),first=4,second=3,n=2,c=2):
    dungeon = cellDungeon(width,height,rand,seed,first,second,n,c)
    while not(connected2(dungeon)):
        dungeon = cellDungeon(width,height,rand,seed,first,second,n,c)

    dungeon = trimDungeon(dungeon)

    height,width = dungeon.shape

    for x in range(0,width):
        for y in range(0,height):
            if dungeon[y,x] == 1:
                dungeon[y,x] = 6

    floodFill(dungeon,0,0,search=6,replace=1)
    return dungeon

if __name__=='__main__':
    printDungeon(cellDungeon(width=20,height=20,first=0,second=5))
    print
    printDungeon(cellDungeon(width=20,height=20,rand=.6,second=1))
    print
    d = cellDungeon(width=10,height=10,first=2,second=0,c=4)
    printDungeon(d)
    printDungeon(trimDungeon(d))
    print(connected(d))