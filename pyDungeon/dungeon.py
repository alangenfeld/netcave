#!/usr/bin/python

# -*- coding: utf-8 -*-
import random, numpy
import pyDungeon.cellular as cellular

# 0 - floor
# 1 - wall
# 2 - unpassable wall
# 3 - open door
# 4 - closed door
# 5 - trapped door
# 6 - inner wall
# 7 - stairs up
# 8 - stairs down
# 9 - spawn


def angDungeon(depth,width=128,height=128,rooms=50,noPrint=False):
    dungeon = numpy.ones((height,width),dtype=numpy.uint)
    roomFlag = numpy.zeros((height,width),dtype=numpy.uint)

    roomList = []

    newRoomList = []

    #generate rooms
    for x in range(0,rooms):
        #print "what?"
        if depth<3:
            room = rectRoom(6,12)
        else:
            #print x
            room = cellular.getRoom(width=int(random.random()*(4+(depth-3))+8+(depth-3)/3),height=int(random.random()*(4+(depth-3))+8+(depth-3)/3),first=2,second=0,c=4)
            #cellular.printDungeon(room)
        roomList = roomList+[room]

    #attempt to place rooms
    for room in roomList:
        loc = [int(random.random()*(width-room.shape[1])), int(random.random()*(height-room.shape[0]))]

        valid = True

        #check if room can be placed
        for x in range(loc[0],loc[0]+room.shape[1]):
            for y in range(loc[1],loc[1]+room.shape[0]):
                if roomFlag[y,x] == 1:
                    valid=False
                    break
            if not(valid):
                break

        if valid:
            #place room
            for x in range(loc[0],loc[0]+room.shape[1]):
                for y in range(loc[1],loc[1]+room.shape[0]):
                    dungeon[y,x] = room[y-loc[1],x-loc[0]]
                    roomFlag[y,x] = 1

            center = loc
            center[0] += room.shape[1]/2
            center[1] += room.shape[0]/2
            newRoomList+=[center]

    #dungeon[newRoomList[len(newRoomList)-1][1],newRoomList[len(newRoomList)-1][0]] = 4

    #Block outer walls
    for xr in range(0,dungeon.shape[1]):
        dungeon[0,xr] = 2
        dungeon[dungeon.shape[0]-1,xr]=2

    for yr in range(0,dungeon.shape[0]):
        dungeon[yr,0] = 2
        dungeon[yr,dungeon.shape[1]-1]=2

    for x in range(0,len(newRoomList)):
        for dest in newRoomList[x+1:]:
            dungeon = tunnel(dungeon,roomFlag,[newRoomList[x][0],newRoomList[x][1]],[dest[0],dest[1]],maxLength=(width+height)/2+4*max(depth-3,0)+3*max(depth-9,0))
          
    while not(cellular.connected2(dungeon)):
        #cellular.printDungeon(dungeon)
        dungeon = angDungeon(depth,width,height,rooms,noPrint=True)
        
    

    if not(noPrint):
        dungeon = placeStairs(dungeon)
        cellular.printDungeon(dungeon)
    
    return dungeon

def rectRoom(minD,maxD):

    rng = maxD-minD

    room = numpy.zeros((random.random()*rng+minD,random.random()*rng+minD),dtype=numpy.uint)

    for xr in range(0,room.shape[1]):
        room[0,xr] = 1;
        room[room.shape[0]-1,xr]=1;

    for yr in range(0,room.shape[0]):
        room[yr,0] = 1;
        room[yr,room.shape[1]-1]=1; 

    return room


def tunnel(dungeon, roomFlag, source, dest, maxLength=128):

    height,width = dungeon.shape

    tunnels = numpy.array(dungeon)

    length = 0;

    loc = source

    maxL = 256

    inRoom = True;

    #tunnel
    while not(loc==dest) and length<maxLength:

        #generate tunnel segment
        direction = [[0,0],0]
        
        pos = [[1,0],[0,1],[-1,0],[0,-1]]
        pos2 = []
        if(random.random() < 0.85):
            if loc[0]<dest[0]:
                pos2+= [[1,0]]
            elif loc[0]>dest[0]:
                pos2+=[[-1,0]]

            if loc[1]<dest[1]:
                pos2+= [[0,1]]
            elif loc[1]>dest[1]:
                pos2+= [[0,-1]]

            direction[0] = pos2[int(random.random()*len(pos2))]
        else:
            direction[0] = pos[int(random.random()*4)]

        temp = int(random.random()*6)
        
        if temp==5:
            direction[1] = int(random.random()*6+4)
        else:
            direction[1] = int(random.random()*min(5,1+abs(loc[0]-dest[0])+abs(loc[1]-dest[1])))
        #print(abs(loc[0]-dest[0])+abs(loc[1]-dest[1]))

        #print('-> '+repr(direction[1]))
        #length += direction[1]

        #place tunnel segment
        for x in range(1,direction[1]+1):
            temp = [0,0]
            temp[0] = loc[0] + direction[0][0]
            temp[1] = loc[1] + direction[0][1]


            #if we haven't encountered an unpassable wall
            if not(tunnels[temp[1],temp[0]] == 2):

                if not(inRoom) and roomFlag[temp[1],temp[0]]==1:
                    inRoom = True
                    tunnels = placeDoor(tunnels,temp,direction[0])
                    tunnels = mark(tunnels,temp,direction[0])

                if inRoom and roomFlag[temp[1],temp[0]]==0:
                    inRoom = False
                    tunnels = placeDoor(tunnels, loc,direction[0])
                    tunnels = mark(tunnels,loc,direction[0])

                if not(inRoom):
                    if dungeon[temp[1],temp[0]]==0 and dungeon[loc[1],loc[0]]==1:
                        tunnels = placeDoor(tunnels, loc,direction[0])
                    elif dungeon[temp[1],temp[0]]==1 and dungeon[loc[1],loc[0]]==0:
                        tunnels = placeDoor(tunnels, temp,direction[0])

                loc=temp
                if tunnels[loc[1],loc[0]] == 1:
                    tunnels[loc[1],loc[0]] = 0
                length+=1
                if loc==dest:
                    break
            else:
                break

    #if tunneling was succesfull, write changes to dungeon
    #print(length)
    if length<maxLength:
        return tunnels

    return dungeon

def placeDoor(dungeon, loc, direction):
    temp = int(random.random()*40)

    if (direction == [1,0] or direction == [-1,0]) and (dungeon[loc[1]+1,loc[0]] == 0 or dungeon[loc[1]-1,loc[0]]==0):
        return dungeon
    elif (direction == [0,-1] or direction == [0,1]) and (dungeon[loc[1],loc[0]+1] == 0 or dungeon[loc[1],loc[0]-1]==0):
        return dungeon

    if temp>15 and temp<30:
        dungeon[loc[1],loc[0]] = 4
    elif temp>=30 and temp<=37:
        dungeon[loc[1],loc[0]] = 3
    elif temp>=38:
        dungeon[loc[1],loc[0]] = 5

    dungeon = mark(dungeon,loc,direction)
    return dungeon

def mark(dungeon,loc,direction):
    if direction == [0,1] or direction == [0,-1]:
        if dungeon[loc[1],loc[0]+1] == 1:
            dungeon[loc[1],loc[0]+1] = 2

        if dungeon[loc[1],loc[0]-1] == 1:
            dungeon[loc[1],loc[0]-1] = 2
    else:
        if dungeon[loc[1]+1,loc[0]] == 1:
            dungeon[loc[1]+1,loc[0]] = 2

        if dungeon[loc[1]-1,loc[0]] == 1:
            dungeon[loc[1]-1,loc[0]] = 2

    return dungeon
    
def placeStairs(dungeon):
    locList = []
    height, width = dungeon.shape
    
    for x in range(1,width-1):
        for y in range(1,height-1):
            if dungeon[y,x]==1:
                typeList = [0,0,0,0,0,0,0,0,0,0]
                typeList[dungeon[y+1,x]] += 1
                typeList[dungeon[y-1,x]] += 1
                typeList[dungeon[y,x+1]] += 1
                typeList[dungeon[y,x-1]] += 1
                if typeList[0]>1 and typeList[0]+typeList[1]+typeList[2] == 4:
                    locList += [(x,y)]
                     
    if len(locList)<2:
        print('Critical Failure - unable to place stairs\n\tGame over man, game over!')
                 
    bestDist = 0
    while bestDist<2:
        randList = []
        for k in range(0,10):
            randList += [locList[int(random.random()*len(locList))]]
            
        bestUp = randList[0]
        bestDown = randList[1]
        bestDist = abs(randList[1][0] - randList[0][0]) + abs(randList[1][1] - randList[0][1])
            
        for j in range(0,10):
            for k in range(j,10):
                if j!=k:
                    dist = abs(randList[j][0] - randList[k][0]) + abs(randList[j][1] - randList[k][1])
                    if dist>bestDist:
                        bestDist = dist
                        bestUp = randList[j]
                        bestDown = randList[k]
                        
    dungeon[bestUp[1],bestUp[0]] = 7
    dungeon[bestDown[1],bestDown[0]] = 8
                    
    if dungeon[bestUp[1]+1,bestUp[0]] == 0:
        dungeon[bestUp[1]+1,bestUp[0]] = 9
    elif dungeon[bestUp[1]-1,bestUp[0]] == 0:
        dungeon[bestUp[1]-1,bestUp[0]] = 9
    elif dungeon[bestUp[1],bestUp[0]+1] == 0:
        dungeon[bestUp[1],bestUp[0]+1] = 9
    elif dungeon[bestUp[1],bestUp[0]-1] == 0:
        dungeon[bestUp[1],bestUp[0]-1] = 9
        
    if dungeon[bestDown[1]+1,bestDown[0]] == 0:
        dungeon[bestDown[1]+1,bestDown[0]] = 9
    elif dungeon[bestDown[1]-1,bestDown[0]] == 0:
        dungeon[bestDown[1]-1,bestDown[0]] = 9
    elif dungeon[bestDown[1],bestDown[0]+1] == 0:
        dungeon[bestDown[1],bestDown[0]+1] = 9
    elif dungeon[bestDown[1],bestDown[0]-1] == 0:
        dungeon[bestDown[1],bestDown[0]-1] = 9
        
    return dungeon
            

if __name__=="__main__":
    cellular.printDungeon(angDungeon(9,64,64,50))
