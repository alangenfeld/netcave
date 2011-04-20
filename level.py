import stupidDungeon,os,random

class floor():
    dungeon = []
    
    def __init__(self, depth):
        self.dungeon = stupidDungeon.getDungeon(os.path.join('DungeonLibrary','L'+repr(depth),repr(int(random.random()*5))))
        
    def getBlock(self, x, y):
        return self.dungeon[y][x]
        
    def isPassable(self, x, y):
        try:
            passable = self.dungeon[y][x] != 1 and self.dungeon[y][x] != 2
        except:
            passable = False

        return passable
        
class level():
    floors = []
    currentFloor = 0
    
    def __init__(self):
        for d in range(0,15):
            self.floors += [floor(d)]
            
    def getFloor(self, depth):
        return self.floors[depth]
        
    def getCurrentFloor(self):
        return self.floors[self.currentFloor]
