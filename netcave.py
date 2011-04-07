import VRScript
import stupidDungeon

CAVE = 3
WIDTH = 32
HEIGHT = 32


#dungeon = stupidDungeon.newDungeon(3, WIDTH, HEIGHT, 25)
dungeon = stupidDungeon.getDungeon()

# Floor 
floor = VRScript.Core.Entity('Floor')
fbox = VRScript.Resources.Box(VRScript.Math.Vector(HEIGHT*CAVE/2,WIDTH*CAVE/2,CAVE/2), 
                              VRScript.Math.Point(0,0,CAVE/2))

floor.attach(VRScript.Core.Renderable('Floor',fbox))
floor.renderable('').show()

phys = VRScript.Core.Physical('Floor', fbox)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
phys.setCollisionType(VRScript.Core.CollisionType.Static)
floor.attach(phys)

# insert floor 

for y in range(len(dungeon)) :
    for x in range(len(dungeon[y])) :
        if dungeon[y][x] == 1 :
            name = 'cube[' + str(y) + '][' + str(x) + ']'
            cube_e = VRScript.Core.Entity(name)
            # translate and attach mesh
            cube_m = VRScript.Resources.Box(VRScript.Math.Vector(1,1,1)*(CAVE/2),
                                            VRScript.Math.Point(((x*CAVE) + CAVE/2) - HEIGHT*CAVE/2,
                                                                ((y*CAVE) + CAVE/2) - WIDTH*CAVE/2,
                                                                CAVE/2))
            
            cube_e.attach(VRScript.Core.Renderable(name,cube_m))
            cube_e.renderable('').show()
            cube_p = VRScript.Core.Physical(name, cube_m)
            cube_p.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
            phys.setCollisionType(VRScript.Core.CollisionType.Static)
            cube_e.attach(cube_p)
            
