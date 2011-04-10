import VRScript
import stupidDungeon

CAVE = 3
WIDTH = 32
HEIGHT = 32


#dungeon = stupidDungeon.newDungeon(3, WIDTH, HEIGHT, 25)
dungeon = stupidDungeon.getDungeon()

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
        if dungeon[y][x] == 0 :
            start = [x,y]
            break
    if not(start == []):
        break
		
start[0] = (WIDTH/2)*CAVE - start[0]*CAVE
start[1] = (HEIGHT/2)*CAVE - start[1]*CAVE
cubelist = []

VRScript.Interaction.setNavigationSpeed(6,0)


           
for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 1 or dungeon[y][x] == 2 :
            name = 'cube[' + str(y) + '][' + str(x) + ']'
            cube_e = VRScript.Core.Entity(name)
            # translate and attach mesh

            cube_e.movable().setPose(VRScript.Math.Matrix().
                                     preTranslation(VRScript.Math.Vector(((x*CAVE + start[0]) + CAVE/2) - HEIGHT*CAVE/2,
                                                                         ((y*CAVE + start[1]) + CAVE/2) - WIDTH*CAVE/2,
                                                                         0)))

            cube_m = VRScript.Resources.Mesh(name, 'cube.osg')
            cube_e.attach(VRScript.Core.Renderable(name,cube_m))
            cube_p = VRScript.Core.Physical(name, VRScript.Resources.BoundingBox(cube_m))
            cube_p.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
            #cube_p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
            cube_e.renderable('').show()
            cubelist  += [cube_e]
            cube_e.attach(cube_p)
            
