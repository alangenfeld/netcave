import stupidDungeon,os,random
import VRScript

class floor():
    dungeon = []
    items = []
    mobs = []
    depth = -1
    CAVE = 0
    wallmap = {}
    start = []
    end = []
    
    def __init__(self, depth, CAVE=3):
        self.depth = depth
        self.CAVE = CAVE
        self.dungeon = stupidDungeon.getDungeon(os.path.join('DungeonLibrary','L'+repr(depth),repr(int(random.random()*5))))
        self.findSpawns()
        self.genWalls()
        self.generateMobs()
        self.generateItems()

        
    def getBlock(self, x, y):
        return self.dungeon[y][x]
        
    def isPassable(self, x, y):
        try:
            passable = self.dungeon[y][x] != 1 and self.dungeon[y][x] != 2
        except:
            passable = False

        return passable
        
    def generateMobs(self):
        pass
    
    def generateItems(self):
        pass
    
    def findSpawns(self):
        for y in range(len(self.dungeon)) :
            for x in range(len(self.dungeon[y])) :
                if self.dungeon[y][x] == 9 :
                    if self.dungeon[y+1][x] == 7 or  self.dungeon[y-1][x] == 7 or self.dungeon[y][x+1] == 7 or  self.dungeon[y][x-1] == 7:
                        self.start = [x,y]
                    if self.dungeon[y+1][x] == 8 or  self.dungeon[y-1][x] == 8 or self.dungeon[y][x+1] == 8 or  self.dungeon[y][x-1] == 8:
                        self.end = [x,y]
                        

            if not(self.start == [] or self.end == []):
                break
                
    def genWalls(self):
        offset = [self.depth*96,self.depth*96]
        self.offset = offset
        entityList = []
        for y in range(len(self.dungeon)) :
            for x in range(len(self.dungeon[y])) :
                if self.dungeon[y][x] == 0 or  self.dungeon[y][x]>=3:
                    entityList  += [self.makeEntity('Floor',x,y,0,offset)]
                    
                    entityList  += [self.makeEntity('Cieling',x,y,0,offset)]
                    
                    if self.dungeon[y-1][x]==1 or self.dungeon[y-1][x]==2:
                        entityList  += [self.makeEntity('RightWall',x,y,0,offset)]
                        
                    if self.dungeon[y+1][x]==1 or self.dungeon[y+1][x]==2:
                        entityList  += [self.makeEntity('LeftWall',x,y,0,offset)]
                        
                    if self.dungeon[y][x+1]==1 or self.dungeon[y][x+1]==2:
                        entityList  += [self.makeEntity('FrontWall',x,y,0,offset)]
                        
                    if self.dungeon[y][x-1]==1 or self.dungeon[y][x-1]==2:
                        entityList  += [self.makeEntity('BackWall',x,y,0,offset)]
    
    def makeEntity(self,typing,x,y,z,offset):
        loc = '[' + str(y) + '][' + str(x) + ']'
        name = typing+loc
        wall_e = VRScript.Core.Entity(name)

        # translate and attach mesh
        wall_e.movable().setPose(VRScript.Math.Matrix().
        preTranslation(VRScript.Math.Vector(((x*self.CAVE) + offset[0]),
                                            ((y*self.CAVE) + offset[1]),
                                            z)))
        print(str((x*self.CAVE) + offset[0])+","+str((y*self.CAVE) + offset[1]))
        wall_m = VRScript.Resources.Mesh(name, typing+'.osg')
        wall_e.attach(VRScript.Core.Renderable(name,wall_m))
        wall_e.renderable('').show()
        if loc in self.wallmap.keys():
            self.wallmap[loc] += [wall_e]
        else:
            self.wallmap[loc] = [wall_e]
            
        #if not(typing=='Floor' or typing=='Cieling'):
        #wall_p = VRScript.Resources.BoundingBox(wall_m)
        #phys = VRScript.Core.Physical('phys'+name, wall_p)
        #phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
        #phys.setCollisionType(VRScript.Core.CollisionType.Static)
        #wall_e.attach(phys)
            
        return wall_e
    
class level():
    floors = []
    currentFloor = 0
    
    def __init__(self):
        for d in range(0,1):
            self.floors += [floor(d)]
            
    def getFloor(self, depth):
        return self.floors[depth]
        
    def getCurrentFloor(self):
        return self.floors[self.currentFloor]
