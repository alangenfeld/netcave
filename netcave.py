import VRScript
import stupidDungeon, level

CAVE = 3
WIDTH = 64
HEIGHT = 64
DELAY = 15
DEVWALL = True
MOVEAMOUNT = 3.0/DELAY
USER = VRScript.Core.Entity('User0')
USERPOS = [0,0]

LEVEL = level.level()
dungeon = LEVEL.getFloor(0).dungeon

class gameController(VRScript.Core.Behavior):
    timer = 0
    moveVec = VRScript.Math.Vector(0,0,0);
    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)
        
    def OnInit(self,info):
        pass
    
    def setLevel(self,level):
        self.level = level
    
    def OnUpdate(self,info):
        if self.timer > 0:
            USER.physical('').applyImpulse(self.moveVec,VRScript.Math.Vector(0,0,0))
            self.timer -= 1    
        if self.timer == 0:
            button =  VRScript.Util.getControllerState(0)['button']
            joystick = VRScript.Util.getControllerState(0)['joystickAxis']
            if DEVWALL:
                if button[0] and button[2] and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]+1):
                    self.moveVec = VRScript.Math.Vector(0,MOVEAMOUNT,0)
                    self.timer=DELAY
                    USERPOS[1] +=1
                elif button[1] and button[2] and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]-1):
                    self.moveVec = VRScript.Math.Vector(0,-MOVEAMOUNT,0)
                    self.timer=DELAY
                    USERPOS[1] -=1
                elif button[0] and not(button[2]) and self.level.getCurrentFloor().isPassable(USERPOS[0]-1,USERPOS[1]):
                    self.moveVec = VRScript.Math.Vector(-MOVEAMOUNT,0,0)
                    self.timer=DELAY
                    USERPOS[0] -=1
                elif button[1] and not(button[2]) and self.level.getCurrentFloor().isPassable(USERPOS[0]+1,USERPOS[1]):
                    self.moveVec = VRScript.Math.Vector(MOVEAMOUNT,0,0)
                    self.timer=DELAY
                    USERPOS[0] +=1
            else:
                if joystick[1] > 0.8  and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]+1):
                    self.moveVec = VRScript.Math.Vector(0,MOVEAMOUNT,0)
                    self.timer=DELAY
                    USERPOS[1] +=1
                elif joystick[1] < -0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]-1):
                    self.moveVec = VRScript.Math.Vector(0,-MOVEAMOUNT,0)
                    self.timer=DELAY
                    USERPOS[1] -=1
                elif joystick[0] < -0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0]-1,USERPOS[1]):
                    self.moveVec = VRScript.Math.Vector(-MOVEAMOUNT,0,0)
                    self.timer=DELAY
                    USERPOS[0] -=1
                elif joystick[0] > 0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0]+1,USERPOS[1]):
                    self.moveVec = VRScript.Math.Vector(MOVEAMOUNT,0,0)
                    self.timer=DELAY
                    USERPOS[0] +=1

def makeEntity(typing,x,y,z,offset):
    name = typing+'[' + str(y) + '][' + str(x) + ']'
    wall_e = VRScript.Core.Entity(name)

    # translate and attach mesh
    wall_e.movable().setPose(VRScript.Math.Matrix().
                        preTranslation(VRScript.Math.Vector((((x*CAVE) + CAVE/2.0) - offset[0]),
                                                            (((y*CAVE) + CAVE/2.0) - offset[1]),
                                                            z)))

    wall_m = VRScript.Resources.Mesh(name, typing+'.osg')
    wall_e.attach(VRScript.Core.Renderable(name,wall_m))
    wall_e.renderable('').show()
    
    #if not(typing=='Floor' or typing=='Cieling'):
        #wall_p = VRScript.Resources.BoundingBox(wall_m)
        #phys = VRScript.Core.Physical('phys'+name, wall_p)
        #phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
        #phys.setCollisionType(VRScript.Core.CollisionType.Static)
        #wall_e.attach(phys)
    
    return wall_e

# Floor 
# floor = VRScript.Core.Entity('Floor')
# fbox = VRScript.Resources.Box(VRScript.Math.Vector(HEIGHT*CAVE/2,WIDTH*CAVE/2,CAVE/2), 
                              # VRScript.Math.Point(0,0,CAVE/2))

# floor.attach(VRScript.Core.Renderable('Floor',fbox))
# floor.renderable('').show()

# phys = VRScript.Core.Physical('Floor', fbox)
# phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
# phys.setCollisionType(VRScript.Core.CollisionType.Static)
# floor.attach(phys)

# insert floor 
VRScript.Core.Entity('e_ground').attach(VRScript.Core.Physical('p_ground',VRScript.Resources.Plane()))
VRScript.Interaction.enableNavigation(False,0)
USER.physical('').setPhysicsProperties(VRScript.Core.PhysicsProperties(1,.1,.1,.1,.2))
start = []

for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 9 :
            start = [x,y]
            USERPOS = [x,y]
            break
    if not(start == []):
        break
		
start[0] = start[0]*CAVE + CAVE/2.0 + 5
start[1] = start[1]*CAVE + CAVE/2.0 + 5

entityList = []

#VRScript.Interaction.setNavigationSpeed(6,0)
#cube_e = VRScript.Core.Entity('blarg')
#cube_m = VRScript.Resources.Box(VRScript.Math.Vector(.5,.5,.5), 
                                            #VRScript.Math.Point(0,
                                                                #0,
                                                                #3.5))
#cube_e.attach(VRScript.Core.Renderable('blarg',cube_m))
#cube_e.renderable('').show()

for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 0 or  dungeon[y][x]>=3:
            entityList  += [makeEntity('Floor',x,y,0,start)]
            
            entityList  += [makeEntity('Cieling',x,y,0,start)]
            
            if dungeon[y-1][x]==1 or dungeon[y-1][x]==2:
                entityList  += [makeEntity('RightWall',x,y,0,start)]
                
            if dungeon[y+1][x]==1 or dungeon[y+1][x]==2:
                entityList  += [makeEntity('LeftWall',x,y,0,start)]
                
            if dungeon[y][x+1]==1 or dungeon[y][x+1]==2:
                entityList  += [makeEntity('FrontWall',x,y,0,start)]
                
            if dungeon[y][x-1]==1 or dungeon[y][x-1]==2:
                entityList  += [makeEntity('BackWall',x,y,0,start)]
gc = gameController()
gc.setLevel(LEVEL)
        #elif dungeon[y][x] == 7 :
            #print('up stairs')
        #if dungeon[y][x] == 9 :
            #name = 'cube[' + str(y) + '][' + str(x) + ']'
            #cube_e = VRScript.Core.Entity(name)

            #cube_m = VRScript.Resources.Box(VRScript.Math.Vector(.5,.5,.5), 
                                            #VRScript.Math.Point((((x*CAVE) + CAVE/2) - start[0]),
                                                                #(((y*CAVE) + CAVE/2) - start[1]),
                                                                #CAVE/2))

            #cube_e.attach(VRScript.Core.Renderable(name,cube_m))
            #cube_e.renderable('').show()

        #elif dungeon[y][x] == 8 :
            #print('down stairs')