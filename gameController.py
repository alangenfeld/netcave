import VRScript

class gameController(VRScript.Core.Behavior):
    timer = 0
    moveVec = VRScript.Math.Vector(0,0,0)
#    torches = {torch(), torch(), torch()}
    DELAY = 15
    MOVEAMOUNT = 3.0/DELAY
    USERPOS = [0,0]
    DEVELOP = False
    CLIP = 8
    
    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)
        
    def OnInit(self,info):
        self.USER = VRScript.Core.Entity('User0')
        self.WAND = VRScript.Core.Entity('User0Hand')
#        self.torches[0].setID(0)
#        self.torches[1].setID(1)
#        self.torches[2].setID(2)
    
#    def setTorch(self, ID, x, y, z) :
#        self.torches[ID].setPos(x, y, z)

    def setLevel(self,level):
        self.level = level
        
    def setDevelop(self,devel):
        self.DEVELOP = devel
        
    def setUserPosition(self,pos):
        self.USERPOS = pos
        wallmap = self.level.getFloor(0).wallmap
        self.showHide([pos[0]-self.CLIP,pos[0]+self.CLIP],[pos[1]-self.CLIP,pos[1]+self.CLIP],True)
                        
    def showHide(self,xrng, yrng, sh):
        wallmap = self.level.getCurrentFloor().wallmap
        for x in range(xrng[0],xrng[1]+1):
            for y in range(yrng[0],yrng[1]+1):
                loc = '[' + str(y) + '][' + str(x) + ']'
                if loc in wallmap.keys():
                    for wall in wallmap[loc]:
                        if sh:
                            wall.renderable('').show()
                        else:
                            wall.renderable('').hide()
        
    def foreward(self):
        self.moveVec = VRScript.Math.Vector(0,self.MOVEAMOUNT,0)
        self.timer=self.DELAY
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]-self.CLIP],False)
        self.USERPOS[1] +=1
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]+self.CLIP,self.USERPOS[1]+self.CLIP],True)
        
    def backward(self):
        self.moveVec = VRScript.Math.Vector(0,-self.MOVEAMOUNT,0)
        self.timer=self.DELAY
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]+self.CLIP,self.USERPOS[1]+self.CLIP],False)
        self.USERPOS[1] -=1
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]-self.CLIP],True)
        
    def left(self):
        self.moveVec = VRScript.Math.Vector(-self.MOVEAMOUNT,0,0)
        self.timer=self.DELAY
        self.showHide([self.USERPOS[0]+self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
        self.USERPOS[0] -=1
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]-self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
        
        
    def right(self):
        self.moveVec = VRScript.Math.Vector(self.MOVEAMOUNT,0,0)
        self.timer=self.DELAY
        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]-self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
        self.USERPOS[0] +=1
        self.showHide([self.USERPOS[0]+self.CLIP,self.USERPOS[0]+self.CLIP],
                 [self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
        
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
            
            #print(repr(USER.movable().getPose().x.w)+","+repr(USER.movable().getPose().y.w))
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
                #print(str(USER.movable().getPose().getTranslation().x)+","+str(USER.movable().getPose().getTranslation().y))
                if (movedir+facedir)%4 == 0:
                    self.foreward()
                elif (movedir+facedir)%4 == 1:
                    self.right()
                elif (movedir+facedir)%4 == 2:
                    self.backward()
                elif (movedir+facedir)%4 == 3:
                    self.left()
                print('\n'+self.getMiniMap())
                    
    def getMiniMap(self):
        USERPOS = self.USERPOS
        mini = ""
        for y in range(USERPOS[1]+4,USERPOS[1]-5,-1):
            narg = ""
            for x in range(USERPOS[0]-4,USERPOS[0]+5):
                if x>=0 and x<64 and y>=0 and y<64:
                    if x==USERPOS[0] and y==USERPOS[1]:
                        narg+='X'
                    else:
                        t = self.level.getCurrentFloor().dungeon[y][x]
                        if t == 0 or t == 9:
                            narg += ' '
                        elif t == 1 or t == 2 or t == 6:
                            narg += '#'
                        elif t == 3:
                            narg += '('
                        elif t == 4 or t == 5:
                            narg += 'D'
                        elif t == 7:
                            narg += '<'
                        elif t == 8:
                            narg += '>'
                else:
                    narg+='#'
            mini += narg + '\n'
        return mini
                
    def OnUpdate(self,info):
        #print(str(self.USER.movable().getPose().getTranslation().x)+","+str(self.USER.movable().getPose().getTranslation().y))    
        if self.timer > 0:
            self.USER.physical('').applyImpulse(self.moveVec,VRScript.Math.Vector(0,0,0))
            self.timer -= 1 
        if self.timer == 0:
            self.moveUser()
