import VRScript
import stupidDungeon

CAVE = 3
WIDTH = 64
HEIGHT = 64


dungeon = stupidDungeon.getDungeon('DungeonLibrary/L1/2')

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

start = []

for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 9 :
            start = [x,y]
            break
    if not(start == []):
        break
		
#start[0] = (WIDTH/2)*CAVE - start[0]*CAVE
#start[1] = (HEIGHT/2)*CAVE - start[1]*CAVE
print(start)
start[0] = start[0]*CAVE# + CAVE/2
start[1] = start[1]*CAVE# + CAVE/2
print(start)

cubelist = []

VRScript.Interaction.setNavigationSpeed(6,0)

for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 1 or dungeon[y][x] == 2 :
            name = 'cube[' + str(y) + '][' + str(x) + ']'
            cube_e = VRScript.Core.Entity(name)
            # translate and attach mesh

#            cube_e.movable().setPose(VRScript.Math.Matrix().
#                                     preTranslation(VRScript.Math.Vector(((x*CAVE + start[0]) + CAVE/2) - HEIGHT*CAVE/2,
#                                                                         ((y*CAVE + start[1]) + CAVE/2) - WIDTH*CAVE/2,
#                                                                         0)))
            cube_e.movable().setPose(VRScript.Math.Matrix().
                                     preTranslation(VRScript.Math.Vector(((x*CAVE) + CAVE/2) - start[0],
                                                                         ((y*CAVE) + CAVE/2) - start[1],
                                                                         -CAVE)))

            cube_m = VRScript.Resources.Mesh(name, 'cube.osg')
            cube_e.attach(VRScript.Core.Renderable(name,cube_m))
            #cube_p = VRScript.Core.Physical(name, VRScript.Resources.BoundingBox(cube_m))
            #cube_p.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
            #cube_p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
            cube_e.renderable('').show()
            #cube_e.attach(cube_p)
            cubelist  += [cube_e]
        elif dungeon[y][x] == 7 :
            print('up stairs')
        elif dungeon[y][x] == 9 :
            name = 'cube[' + str(y) + '][' + str(x) + ']'
            cube_e = VRScript.Core.Entity(name)

            cube_m = VRScript.Resources.Box(VRScript.Math.Vector(.5,.5,.5), 
                                            VRScript.Math.Point(x*CAVE,y*CAVE,CAVE/2))

            cube_e.attach(VRScript.Core.Renderable(name,cube_m))
            cube_e.renderable('').show()

        elif dungeon[y][x] == 8 :
            print('down stairs')
