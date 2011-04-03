import VRScript

# ------------------------ FLOOR ------------------------ #

# Create a floor entity
floor = VRScript.Core.Entity('e_floor')

# Create a matrix which will be used later to scale the floor model
floorScaleMatrix = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(50, 50, 1))

# Create a renderable mesh for the floor
floorMesh = VRScript.Resources.Mesh('m_floor','ground-plane.osg', floorScaleMatrix)
# Attach the mesh to the floor entity
floor.attach(VRScript.Core.Renderable('r_floor', floorMesh))
# Enable rendering of the floor mesh
floor.renderable('').show()

# Create physical behavior for the floor
floorPhysical = VRScript.Resources.Plane()
# Attach the behavior to the floor entity
floor.attach(VRScript.Core.Physical('p_floor', floorPhysical))
# Create a physics property set (Mass, Friction, Linear Damping, Angular Damping, Restitution)
floorPhysicsProps = VRScript.Core.PhysicsProperties(0,.9,1,1,.5)
# Apply that property set to the physics behavior
floor.physical('').setPhysicsProperties(floorPhysicsProps)

floor.movable().setPose(VRScript.Math.Matrix().preTranslation(VRScript.Math.Vector(0,0,-.5)))

# Short version, alternate (invisible) ground
#VRScript.Core.Entity('e_ground').attach(VRScript.Core.Physical('p_ground',VRScript.Resources.Plane()))

# ------------------------- END ------------------------- #
