import VRScript
import torch

class gameController(VRScript.Core.Behavior):
    timer = 0
    moveVec = VRScript.Math.Vector(0,0,0)
    torches = []
    DELAY = 15
    MOVEAMOUNT = 3.0/DELAY
    USERPOS = [0,0]
    CLIP = 8
    
    def init(self, entity=None):
        VRScript.Core.Behavior.init(self,entity)
        
    def OnInit(self,info):
        self.USER = VRScript.Core.Entity('User0')
        self.WAND = VRScript.Core.Entity('User0Hand')
        for x in range(4):
            self.torches+=[torch.torch()]
            self.torches[x].setID(x)
        self.currentTorch = 0
        self.waitTorch = 0

        # Minimap stuff

        m = VRScript.Math.Matrix()
        m = m.postScale( VRScript.Math.Vector( .5, .5, .5 ))
        m = m.postTranslation( VRScript.Math.Vector( 0, -2, .5 ))
        m = m.postAxisAngle( 180, VRScript.Math.Vector(0,0,1) )
        m = m.postAxisAngle( 180, VRScript.Math.Vector(0,1,0,) )
        m = m.postAxisAngle( 90, VRScript.Math.Vector(1,0,0,) )
 
        self.minimap = VRScript.Core.FontText( "MiniMap", "", "VeraMono.ttf", m )
        self.minimap.setColor(VRScript.Core.Color( 1,1, 1,1))
        self.USER.attach( self.minimap )
        self.minimap.show()
        
    
    def setTorch(self, ID, x, y, z) :
        print(ID)
        self.torches[ID].setPos(x, y, z)
        # set light

    def setLevel(self,level):
        self.level = level
        
    def setUserPosition(self,pos):
        self.USERPOS[0] = pos[0]
        self.USERPOS[1] = pos[1]
        wallmap = self.level.getCurrentFloor().wallmap
        self.showHide([pos[0]-self.CLIP,pos[0]+self.CLIP],[pos[1]-self.CLIP,pos[1]+self.CLIP],True)
                        
    def showHide(self,xrng, yrng, sh):
        pass
        #wallmap = self.level.getCurrentFloor().wallmap
        #for x in range(xrng[0],xrng[1]+1):
            #for y in range(yrng[0],yrng[1]+1):
                #loc = '[' + str(y) + '][' + str(x) + ']'
                #if loc in wallmap.keys():
                    #for wall in wallmap[loc]:
                        #if sh:
                            #wall.renderable('').show()
                        #else:
                            #wall.renderable('').hide()
                            
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
        self.devButton()
        if not joystick:
            if button[0] and button[2]:
                movedir = 0
            elif button[1] and button[2]:
                movedir = 2
            elif button[0] and not(button[2]):
                movedir = 3
            elif button[1] and not(button[2]):
                movedir = 1
        else:
            if joystick[1] > 0.8:
                movedir = 0
            elif joystick[1] < -0.8:
                movedir = 2
            elif joystick[0] < -0.8:
                movedir = 3
            elif joystick[0] > 0.8:
                movedir = 1
        
        if movedir>=0:
            #print(str(USER.movable().getPose().getTranslation().x)+","+str(USER.movable().getPose().getTranslation().y))
            if (movedir+facedir)%4 == 0  and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]+1):
                self.foreward()
            elif (movedir+facedir)%4 == 1 and self.level.getCurrentFloor().isPassable(USERPOS[0]+1,USERPOS[1]):
                self.right()
            elif (movedir+facedir)%4 == 2 and self.level.getCurrentFloor().isPassable(USERPOS[0],USERPOS[1]-1):
                self.backward()
            elif (movedir+facedir)%4 == 3 and self.level.getCurrentFloor().isPassable(USERPOS[0]-1,USERPOS[1]):
                self.left()

                
            self.minimap.setText( self.getMiniMap(11))
            print(USER.movable().getPose().getTranslation().x,USER.movable().getPose().getTranslation().y)

    def getMiniMap(self, size):
        USERPOS = self.USERPOS
        mini = ""
        for y in range(USERPOS[1]+size,USERPOS[1]-size-1,-1):
            narg = ""
            for x in range(USERPOS[0]-size,USERPOS[0]+size+1):
                if x>=0 and x<len(self.level.getCurrentFloor().dungeon) and y>=0 and y<len(self.level.getCurrentFloor().dungeon[0]):
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
        return mini[:-1]
        
    def OnUpdate(self,info):
        #print(str(self.USER.movable().getPose().getTranslation().x)+","+str(self.USER.movable().getPose().getTranslation().y))    
        if self.timer > 0:
#            if self.timer == 1 and len(self.level.getCurrentFloor().mobs)==0:
            if self.timer == 1 and not self.level.getCurrentFloor().mobAlive:
                self.level.getCurrentFloor().generateMobs(self.USERPOS)
                
            if self.timer == int(self.DELAY/2)+1:
                
                #print(self.level.getCurrentFloor().dungeon[self.USERPOS[1]][self.USERPOS[0]])
                if self.level.getCurrentFloor().dungeon[self.USERPOS[1]][self.USERPOS[0]]==7:
                    if self.level.canGoUp():
                        print('going up')
                        self.level.goUp()
                        self.moveVec = self.level.getCurrentFloor().move2Spawn(self.USER,self.MOVEAMOUNT, int(self.DELAY/2) * self.MOVEAMOUNT ,down=False)
                        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],[self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
                        self.setUserPosition(self.level.getCurrentFloor().end)
                        
                elif self.level.getCurrentFloor().dungeon[self.USERPOS[1]][self.USERPOS[0]]==8:
                    if self.level.canGoDown():
                        print('going down')
                        self.level.goDown()
                        self.moveVec = self.level.getCurrentFloor().move2Spawn(self.USER,self.MOVEAMOUNT, int(self.DELAY/2) * self.MOVEAMOUNT)
                        self.showHide([self.USERPOS[0]-self.CLIP,self.USERPOS[0]+self.CLIP],[self.USERPOS[1]-self.CLIP,self.USERPOS[1]+self.CLIP],True)
                        self.setUserPosition(self.level.getCurrentFloor().start)
                else:
                    self.USER.physical('').applyImpulse(self.moveVec,VRScript.Math.Vector(0,0,0))
            else:
                self.USER.physical('').applyImpulse(self.moveVec,VRScript.Math.Vector(0,0,0))
            self.timer -= 1 
            
        if self.timer == 0:
            self.moveUser()
            
        pos = self.USER.movable().getPose().getTranslation()
        
        for x in range(len(self.torches)):
            torch = self.torches[x]
            self.level.setLight( x, ( torch.x-pos.x, torch.z-pos.z, -torch.y+pos.y, 1 ) )
            #print(str(x)+' '+str(( torch.x-pos.x, torch.z-pos.z, -torch.y+pos.y, 1 )))
        self.level.updateLights()
        
        if self.waitTorch>0:
            self.waitTorch-=1
        #self.level.setLight( 1, ( 0, 0, -9, 1 ) )

    def OnButtonPress(self, cbInfo, btnInfo, intInfo):
        print(str(btnInfo.button))
        if (btnInfo.button == 4 and self.timer==0 and self.waitTorch==0):
            pos = self.USERPOS
            face = self.getFacing()
            x = pos[0] * 3
            y = pos[1] * 3
            if face is 0 : # forward
                if self.level.getCurrentFloor().isPassable(pos[0],pos[1]+1): return
                y += 3.0/2
            elif face is 3 : # left
                if self.level.getCurrentFloor().isPassable(pos[0]-1,pos[1]): return
                x -= 3.0/2
            elif face is 1 : # right
                if self.level.getCurrentFloor().isPassable(pos[0]+1,pos[1]): return
                x += 3.0/2
            else : # back
                if self.level.getCurrentFloor().isPassable(pos[0],pos[1]-1): return
                y -= 3.0/2

            self.setTorch(self.currentTorch, x, y, 3.0/2)
            self.currentTorch = (self.currentTorch + 1) % 4
            self.waitTorch = 5
            
    def devButton(self):
        button =  VRScript.Util.getControllerState(0)['button']
        if (button[0] and button[1] and self.waitTorch==0):
            print('placing '+str(self.currentTorch))
            pos = self.USERPOS
            face = self.getFacing()
            x = pos[0] * 3
            y = pos[1] * 3
            if face is 0 : # forward
                if self.level.getCurrentFloor().isPassable(pos[0],pos[1]+1): return
                #y += 3.0/2
            elif face is 3 : # left
                if self.level.getCurrentFloor().isPassable(pos[0]-1,pos[1]): return
                #x -= 3.0/2
            elif face is 1 : # right
                if self.level.getCurrentFloor().isPassable(pos[0]+1,pos[1]): return
                #x += 3.0/2
            else : # back
                if self.level.getCurrentFloor().isPassable(pos[0],pos[1]-1): return
                #y -= 3.0/2

            self.setTorch(self.currentTorch, x, y, 3.0/2)
            self.currentTorch = (self.currentTorch + 1) % 4
            self.waitTorch = 5

            user = self.USER.movable().getPose().getTranslation()
            print( "User: %f %f %f" % (user.x, user.y, user.z))
            print( "Light: %f %f %f" % (x, y, 3.0/2 ))

