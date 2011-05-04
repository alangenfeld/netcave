import stupidDungeon,os,random
import VRScript
#import Enemy

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

class floor():
    dungeon = []
    items = []
    mobs = []
    depth = -1
    CAVE = 0
    wallmap = {}
    start = []
    end = []
    light_radius_mean = .5
    light_radius_dev = .1
    
    def __init__(self, depth, CAVE=3):
        self.depth = depth
        self.CAVE = CAVE
        
        self.wallList = []
        self.top_entity = VRScript.Core.Entity("DLEVEL")
        m = VRScript.Resources.Mesh('DLEVEL_m', 'floor.osg')
        self.top_entity.attach(VRScript.Core.Renderable("DLEVEL_f", m))
        
        self.level_material = VRScript.Core.MaterialProperties()
        
        self.dungeon = stupidDungeon.getDungeon(os.path.join('DungeonLibrary','L'+repr(depth),repr(int(random.random()*5))))
        self.genWalls()
        self.findSpawns()
        self.generateItems()
        
        self.setLight( [(0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 1)] )
        
    def setLight( self, lights ):

        
        #flicker = random.gauss(self.light_radius_mean,self.light_radius_dev) 
        flicker = 1

        self.level_material.ambientColor = VRScript.Core.Color( lights[0][0],
                                                                lights[0][1],
                                                                lights[0][2],
                                                                flicker)
                                                                
        self.level_material.diffuseColor = VRScript.Core.Color( lights[1][0],
                                                                lights[1][1],
                                                                lights[1][2],
                                                                flicker)
                                                                
        self.level_material.specularColor = VRScript.Core.Color( lights[2][0],
                                                                 lights[2][1],
                                                                 lights[2][2],
                                                                 flicker)
                                                                
        self.level_material.emissiveColor = VRScript.Core.Color( lights[3][0],
                                                                  lights[3][1],
                                                                  lights[3][2],
                                                                  flicker)
        
        
        #self.top_entity.renderable().setMaterialProperties( self.level_material )
        for e in self.wallList:
            e.renderable().setMaterialProperties( self.level_material )
        
        
    def getBlock(self, x, y):
        return self.dungeon[y][x]
        
    def isPassable(self, x, y):
        try:
            passable = self.dungeon[y][x] != 1 and self.dungeon[y][x] != 2
        except:
            passable = False

        return passable
        
    def generateMobs(self, userPosition):
        #don't generate mobs every step or user will never get downtime
        if random.random()<0.2:
            spawnPLocs = []
            spawnLocs = []
            for y in range(userPosition[0]-9,userPosition[1]+9+1) :
                for x in range(userPosition[1]-9,userPosition[1]+9+1) :
                    if x>=0 and x<len(self.dungeon) and y>=0 and y<len(self.dungeon[0]):
                        if self.dungeon[y][x] == 0 and abs(userPosition[0]-x)+abs(userPosition[1]-y)>=6: 
                            spawnPLocs +=[[x,y]]

            rm = int(random.random()*4.0)#int(random.random()*self.depth/5.0)+1
            if rm>3:
                rm = 2
            else:
                rm = 1
            while(len(spawnLocs)<rm):
                consider = spawnPLocs[int(random.random()*len(spawnPLocs))]
                if consider in spawnLocs:
                    continue
                if self.isPassable(y+1,x) and self.isPassable(y-1,x) and self.isPassable(y,x+1) and self.isPassable(y,x-1):
                    spawnLocs += consider
                else:
                    if random.random()<.5:
                        spawnLocs += consider
            
            print(spawnLocs)   
            #generate mob classes
            ## Enemy.spawnLoc("AntLion", "BugMove.fbx", spawnPLocs[0][0]*3, spawnPLocs[0][1]*3)    
            #make sure you add mobs to the mobs list, and remove them when they die
    
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
                
    def move2Spawn(self,USER,MOVEAMOUNT,off,down=True):
        if down:
            st = self.start
        else:
            st = self.end

        x = st[0]*self.CAVE+self.depth*(len(self.dungeon)+32)
        y = st[1]*self.CAVE+self.depth*(len(self.dungeon[0])+32)

        j = st[0]
        k = st[1]
        movedir = VRScript.Math.Vector(0,0,0)
        
        if self.dungeon[k][j+1]==9:
            x-=off
            movedir = VRScript.Math.Vector(MOVEAMOUNT,0,0)
        elif self.dungeon[k][j-1]==9:
            x+=off
            movedir = VRScript.Math.Vector(-MOVEAMOUNT,0,0)
        elif self.dungeon[k+1][j]==9:
            y-=off
            movedir = VRScript.Math.Vector(0,MOVEAMOUNT,0)
        elif self.dungeon[k-1][j]==9:
            y+=off
            movedir = VRScript.Math.Vector(0,-MOVEAMOUNT,0)
        
        trans = USER.movable().getPose().getTranslation()
        loc =  VRScript.Math.Vector(trans.x,trans.y,0,0)
        loc2 = VRScript.Math.Vector(x,y,0,0)
        USER.physical('').applyImpulse(loc2-loc,VRScript.Math.Vector(0,0,0))
        
        return movedir
                
    def genWalls(self):
        offset = [self.depth*(len(self.dungeon)+32),self.depth*(len(self.dungeon[0])+32)]
        self.offset = offset

        for y in range(len(self.dungeon)) :
            for x in range(len(self.dungeon[y])) :
                if self.dungeon[y][x] == 0 or  self.dungeon[y][x]>=3:
                    
                    if not(self.dungeon[y][x]==7 or self.dungeon[y][x]==8):
                        self.wallList  += [self.makeEntity('Floor',x,y,0,offset)]
                    elif not(self.dungeon[y][x]==8):
                        self.wallList  += [self.makeEntity('Stairsup',x,y,0,offset)]
                    
                    if not(self.dungeon[y][x]==8 or self.dungeon[y][x]==7):
                        self.wallList  += [self.makeEntity('Cieling',x,y,0,offset)]
                    elif not(self.dungeon[y][x]==7):
                        self.wallList  += [self.makeEntity('Stairsdown',x,y,0,offset)]
                    
                    if self.dungeon[y-1][x]==1 or self.dungeon[y-1][x]==2:
                        self.wallList  += [self.makeEntity('RightWall',x,y,0,offset)]
                        
                    if self.dungeon[y+1][x]==1 or self.dungeon[y+1][x]==2:
                        self.wallList  += [self.makeEntity('LeftWall',x,y,0,offset)]
                        
                    if self.dungeon[y][x+1]==1 or self.dungeon[y][x+1]==2:
                        self.wallList  += [self.makeEntity('FrontWall',x,y,0,offset)]
                        
                    if self.dungeon[y][x-1]==1 or self.dungeon[y][x-1]==2:
                        self.wallList  += [self.makeEntity('BackWall',x,y,0,offset)]
                        
                    if self.dungeon[y][x] >=3 and self.dungeon[y][x] <=5:
                        self.wallList += [self.makeEntity('Doorway',x,y,0,offset)]
                        self.wallList += [self.makeEntity('Door',x,y,0,offset)]
                        
    def makeEntity(self,typing,x,y,z,offset):
        loc = '[' + str(y) + '][' + str(x) + ']'
        name = typing+loc+':'+str(self.depth)
        wall_e = VRScript.Core.Entity(name)

        # translate and attach mesh
        if (typing == 'Door' or typing == 'Doorway') and self.isPassable(x-1,y) and self.isPassable(x+1,y):
            wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(90,0,0))
            wall_e.movable().setPose(VRScript.Math.Matrix().preTranslation(VRScript.Math.Vector(((x*self.CAVE) + offset[0]),
                                                ((y*self.CAVE) + offset[1]),
                                                z))*wall_e.movable().getPose())
                                                
                                                
        elif typing == 'Stairsup':
            if self.dungeon[y+1][x]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(90,0,0))
            elif self.dungeon[y][x-1]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(180,0,0))
            elif self.dungeon[y-1][x]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(270,0,0))
            wall_e.movable().setPose(VRScript.Math.Matrix().preTranslation(VRScript.Math.Vector(((x*self.CAVE) + offset[0]),
                                                ((y*self.CAVE) + offset[1]),
                                                z))*wall_e.movable().getPose())
        elif typing == 'Stairsdown':
            if self.dungeon[y+1][x]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(90,0,0))
            elif self.dungeon[y][x-1]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(180,0,0))
            elif self.dungeon[y-1][x]==9:
                wall_e.movable().setPose(VRScript.Math.Matrix().preEuler(270,0,0))
            wall_e.movable().setPose(VRScript.Math.Matrix().preTranslation(VRScript.Math.Vector(((x*self.CAVE) + offset[0]),
                                                ((y*self.CAVE) + offset[1]),
                                                z))*wall_e.movable().getPose())
        else:
            wall_e.movable().setPose(VRScript.Math.Matrix().
                                    preTranslation(VRScript.Math.Vector(((x*self.CAVE) + offset[0]),
                                                                       ((y*self.CAVE) + offset[1]),
                                                                       z)))

        
        #print(str((x*self.CAVE) + offset[0])+","+str((y*self.CAVE) + offset[1]))
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
        
        wall_e.movable().setParent( self.top_entity )
            
        return wall_e
        
class level():
    floors = []
    currentFloor = 0
    lights = [(),(),(),()]
    
    def __init__(self):
        for d in range(0,1):
            self.floors += [floor(d)]
            
    def getFloor(self, depth):
        return self.floors[depth]
        
    def getCurrentFloor(self):
        return self.floors[self.currentFloor]
        
    def canGoUp(self):
        return self.currentFloor>0
        
    def canGoDown(self):
        return self.currentFloor<14
        
    def goDown(self):
        self.currentFloor+=1
        if len(self.floors)==self.currentFloor:
            self.floors += [floor(self.currentFloor)]
        return self.floors[self.currentFloor]
        
    def goUp(self):
        self.currentFloor-=1
        return self.floors[self.currentFloor]
        
    def setLight( self, light, pos ):
        self.lights[light] = pos
        
    def updateLights(self):
        self.floors[self.currentFloor].setLight( self.lights )
     
