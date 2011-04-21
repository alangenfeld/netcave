import VRScript

class gameController(VRScript.Core.Behavior):
    timer = 0
    moveVec = VRScript.Math.Vector(0,0,0)
    torches = {torch(), torch(), torch()}
    DELAY = 15
    MOVEAMOUNT = 3.0/DELAY
    USERPOS = [0,0]
    DEVELOP = False
    
    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)
        
    def OnInit(self,info):
        self.USER = VRScript.Core.Entity('User0')
        self.WAND = VRScript.Core.Entity('User0Hand')
        self.torches[0].setID(0)
        self.torches[1].setID(1)
        self.torches[2].setID(2)
    
    def setTorch(self, ID, x, y, z) :
        self.torches[ID].setPos(x, y, z)

    def setLevel(self,level):
        self.level = level
        
    def setDevelop(self,devel):
        self.DEVELOP = devel
        
    def setUserPosition(self,pos):
        self.USERPOS = pos
        
    def foreward(self):
        self.moveVec = VRScript.Math.Vector(0,self.MOVEAMOUNT,0)
        self.timer=self.DELAY
        self.USERPOS[1] +=1
        
    def backward(self):
        self.moveVec = VRScript.Math.Vector(0,-self.MOVEAMOUNT,0)
        self.timer=self.DELAY
        self.USERPOS[1] -=1
        
    def left(self):
        self.moveVec = VRScript.Math.Vector(-self.MOVEAMOUNT,0,0)
        self.timer=self.DELAY
        self.USERPOS[0] -=1
        
    def right(self):
        self.moveVec = VRScript.Math.Vector(self.MOVEAMOUNT,0,0)
        self.timer=self.DELAY
        self.USERPOS[0] +=1
        
    def getFacing(self):
        WAND = self.WAND
        angle = WAND.movable().getPose().getEuler().x
        
        if angle<=45 and angle>-45:
            return 0
        elif angle<=135 and angle>45:
            return 3
        elif angle<=-45 and angle>-135:
            return 1
        else:
            return 2
        
    def moveUser(self):
            USER = self.USER
            
            USERPOS = self.USERPOS
            button =  VRScript.Util.getControllerState(0)['button']
            joystick = VRScript.Util.getControllerState(0)['joystickAxis']
            
            movedir = -1
            facedir = self.getFacing()
            if self.DEVELOP or not joystick:
                if button[0] and button[2] and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]+1):
                    movedir = 0
                elif button[1] and button[2] and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]-1):
                    movedir = 2
                elif button[0] and not(button[2]) and self.level.getCurrentFloor().isPassable(USERPOS[0]-1,USERPOS[1]):
                    movedir = 3
                elif button[1] and not(button[2]) and self.level.getCurrentFloor().isPassable(USERPOS[0]+1,USERPOS[1]):
                    movedir = 1
            else:
                if joystick[1] > 0.8  and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]+1):
                    movedir = 0
                elif joystick[1] < -0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]-1):
                    movedir = 2
                elif joystick[0] < -0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0]-1,USERPOS[1]):
                    movedir = 3
                elif joystick[0] > 0.8 and self.level.getCurrentFloor().isPassable(USERPOS[0]+1,USERPOS[1]):
                    movedir = 1
            
            if movedir>=0:
                if (movedir+facedir)%4 == 0:
                    self.foreward()
                elif (movedir+facedir)%4 == 1:
                    self.right()
                elif (movedir+facedir)%4 == 2:
                    self.backward()
                elif (movedir+facedir)%4 == 3:
                    self.left()
                
    def OnUpdate(self,info):
        if self.timer > 0:
            self.USER.physical('').applyImpulse(self.moveVec,VRScript.Math.Vector(0,0,0))
            self.timer -= 1    
        if self.timer == 0:
            self.moveUser()
