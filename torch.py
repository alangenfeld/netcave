import VRScript

class torch(VRScript.Core.Behavior):
    ID = 0
    x = 0
    y = 0
    z = 0

    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)

    def setID(self,ID):
        self.ID = ID

    def setPos(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def OnInit(self,info):
        name = 'torch' + str(self.ID)
        torch_e = VRScript.Core.Entity(name)
        torch_m = VRScript.Resources.Mesh(name,'torch.osg')        
        torch_e.movable().setPose(VRScript.Math.Matrix().
                                 preTranslation(VRScript.Math.Vector(self.x, self.y, self.z)))

        torch_e.attach(VRScript.Core.Renderable(name, torch_m))
        torch_e.renderable('').show()


    def OnUpdate(self,info):
        name = 'torch' + str(self.ID)
        torch_e = VRScript.Core.Entity(name)
        torch_e.movable().setPose(VRScript.Math.Matrix().
                                 preTranslation(VRScript.Math.Vector(self.x, self.y, self.z)))
        
