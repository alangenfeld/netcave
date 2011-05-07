import VRScript

class torch():
    ID = 0
    x = 0
    y = 0
    z = 0
    name = ''

    def __init__(self):
        pass

    def setID(self,ID):
        self.ID = ID
        self.name = 'torch' + str(self.ID)
        torch_e = VRScript.Core.Entity(self.name)
        torch_m = VRScript.Resources.Mesh(self.name,'torch.osg')        
        torch_e.movable().setPose(VRScript.Math.Matrix().
                                 preTranslation(VRScript.Math.Vector(self.x, self.y, self.z)))

        torch_e.attach(VRScript.Core.Renderable(self.name, torch_m))
        torch_e.renderable('').show()

    def setPos(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z
        size = 60
        torch_e = VRScript.Core.Entity(self.name)
        mat = VRScript.Math.Matrix()
        mat.preScale(VRScript.Math.Vector(size, size, size))
        mat.preTranslation(VRScript.Math.Vector(self.x, self.y, self.z))
        torch_e.movable().setPose(mat)
                                  
        
