import VRScript

CAVE = 3

# Floor 
floor = VRScript.Core.Entity('Floor')
fbox=VRScript.Resources.Box(VRScript.Math.Vector(1,1,1)*10, VRScript.Math.Point(0,0,-10))
floor.attach(VRScript.Core.Renderable('Floor',fbox))
floor.renderable('').show()

phys = VRScript.Core.Physical('Floor', fbox)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
floor.attach(phys)


# Cube test
cube_e = VRScript.Core.Entity('cube')
cube_m = VRScript.Resources.Box(VRScript.Math.Vector(1,1,1)*CAVE, VRScript.Math.Point(0,0,0))
cube_e.attach(VRScript.Core.Renderable('cube',cube_m))
cube_e.renderable('').show()


