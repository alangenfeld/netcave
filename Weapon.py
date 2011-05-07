import VRScript

# ------------------------ Weapon ------------------------ #
class Weapon(VRScript.Core.Behavior):
        def __init__(self, entity, filename, weaponType, atkDamage):
                VRScript.Core.Behavior.__init__(self,entity)
                self.filename = filename
                self.weaponType = weaponType
                self.atkDamage = atkDamage
                self.movable().setParent('User0Hand')
                self.hidden = False
                self.type = "item"

        def OnInit(self, info):
                self.wandMatrix = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(1, 1, 1)*.2)
                self.wandMesh = VRScript.Resources.Mesh(self.getName(),self.filename, self.wandMatrix)
                self.wandRend = VRScript.Core.Renderable(self.getName(), self.wandMesh)
                self.attach(self.wandRend)
                # self.attach(VRScript.Core.Interactible(self.getName(), self.wandRend))
##                self.interactible('').enableGrab(False)
##                self.interactible('').enableSelection(False)
                VRScript.Core.Entity('User0Hand').renderable('User0Hand').hide()
                self.wandRend.show()
                # phys = VRScript.Core.Physical(self.getName(), VRScript.Resources.BoundingBox(self.wandMesh))
####                phys.enableDebugVisual(True)
#                
                # phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(7.5, 0.5, 0.5, 0.6, 0.5))
                # phys.setCollisionType(VRScript.Core.CollisionType.Static)
                # phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
                # self.attach(phys)
##                self.attach(VRScript.Core.Animable(self.getName(), self.wandMesh))

        def getProperties(self):
                return self.type

Weapon("Crowbar", './crowbar.ive', "melee", 21)
