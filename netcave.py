import VRScript
import stupidDungeon, level
from gameController import gameController
#import Weapon

CAVE = 3
WIDTH = 64
HEIGHT = 64
DEVELOP = True


LEVEL = level.level()
dungeon = LEVEL.getFloor(0).dungeon
    


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
#USER.physical('').setPhysicsProperties(VRScript.Core.PhysicsProperties(1,.1,.1,.1,.2))
start = []

# load lights
base_lights = VRScript.Core.Entity( "BASE_LIGHTS" )
base_lights_r = VRScript.Resources.Mesh( "BASE_LIGHTS_r", "OSG_Light_0_3.osg")
base_lights.attach( VRScript.Core.Renderable( "BASE_LIGHTS_r", base_lights_r ) )
base_lights.renderable('').show()

real_lights = []

for light in range( 4 ):
    real_lights.append( VRScript.Core.Entity( "Light_%d" % (light+1) ) )
    light_r = VRScript.Resources.Mesh( "LIGHT_r_%d" % (light+1), "OSG_Light_%d.osg" % (light+4))
    real_lights[light].attach( VRScript.Core.Renderable( "LIGHT_r_%d" % (light+1), light_r ) )
    real_lights[light].renderable('').show()


gc = gameController()
gc.setLevel(LEVEL)

start = LEVEL.getFloor(0).start
gc.setUserPosition(start)
    
#move user to spawn
#print(start[0]*CAVE,start[1]*CAVE)

loc =  VRScript.Math.Vector(-5,-5,0,0)
loc2 = VRScript.Math.Vector(start[0]*CAVE,start[1]*CAVE,loc.z,loc.w)
VRScript.Core.Entity('User0').physical('').applyImpulse(loc2-loc,VRScript.Math.Vector(0,0,0))

#start[0] = 0#start[0]*CAVE
#start[1] = 0#start[1]*CAVE   



entityList = []
print('Loading Finished')
#VRScript.Interaction.setNavigationSpeed(6,0)
#cube_e = VRScript.Core.Entity('blarg')
#cube_m = VRScript.Resources.Box(VRScript.Math.Vector(.5,.5,.5), 
                                            #VRScript.Math.Point(0,
                                                                #0,
                                                                #3.5))
#cube_e.attach(VRScript.Core.Renderable('blarg',cube_m))
#cube_e.renderable('').show()

#for y in range(len(dungeon)) :
    #for x in range(len(dungeon[y])) :
        #if dungeon[y][x] == 0 or  dungeon[y][x]>=3:
            #entityList  += [makeEntity('Floor',x,y,0,start)]
            
            #entityList  += [makeEntity('Cieling',x,y,0,start)]
            
            #if dungeon[y-1][x]==1 or dungeon[y-1][x]==2:
                #entityList  += [makeEntity('RightWall',x,y,0,start)]
                
            #if dungeon[y+1][x]==1 or dungeon[y+1][x]==2:
                #entityList  += [makeEntity('LeftWall',x,y,0,start)]
                
            #if dungeon[y][x+1]==1 or dungeon[y][x+1]==2:
                #entityList  += [makeEntity('FrontWall',x,y,0,start)]
                
            #if dungeon[y][x-1]==1 or dungeon[y][x-1]==2:
                #entityList  += [makeEntity('BackWall',x,y,0,start)]

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
