import VRScript

class torch(VRScript.Core.Behavior):
    ID = 0

    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)

    def setID(ID):
        self.ID = ID

    def setPos(x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def OnInit(self,info):
        name = 'torch' + str(ID)
        torch_e = VRScript.Core.Entity(name)
        torch_m = VRScript.Resources.Mesh(name,'torch.osg')        
        wall_e.movable().setPose(VRScript.Math.Matrix().
                                 preTranslation(VRScript.Math.Vector(self.x, self.y, self.z)))

        torch_e.attach(VRScript.Core.Renderable(name, torch_m))
        wall_e.renderable('').show()


    def OnUpdate(self,info):
        name = 'torch' + str(ID)
        torch_e = VRScript.Core.Entity(name)
        wall_e.movable().setPose(VRScript.Math.Matrix().
                                 preTranslation(VRScript.Math.Vector(self.x, self.y, self.z)))
        
