#import VRScript
import stupidDungeon

CAVE = 3
WIDTH = 16
HEIGHT = 16


#dungeon = stupidDungeon.newDungeon(1, WIDTH, HEIGHT, 15)
dungeon = stupidDungeon.getDungeon()

# Floor 
floor = VRScript.Core.Entity('Floor')
fbox = VRScript.Resources.Box(VRScript.Math.Vector(HEIGHT*CAVE/2,WIDTH*CAVE/2,CAVE/2), 
                              VRScript.Math.Point(0,0,CAVE/2))

floor.attach(VRScript.Core.Renderable('Floor',fbox))
floor.renderable('').show()

phys = VRScript.Core.Physical('Floor', fbox)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
floor.attach(phys)


for y in dungeon :
    for x in y :
        if dungeon[y][x] == 1 :
            cube_e = VRScript.Core.Entity('cube['+y+']['+x+']')
            cube_m = VRScript.Resources.Box(VRScript.Math.Vector(1,1,1)*(CAVE/2),
                                            VRScript.Math.Point((x*CAVE) + CAVE/2,
                                                                (y*CAVE) + CAVE/2,
                                                                CAVE/2))
            
            cube_e.attach(VRScript.Core.Renderable('cube['+y+']['+x+']',cube_m))
            cube_e.renderable('').show()
            cube_e.attach(phys)
            
