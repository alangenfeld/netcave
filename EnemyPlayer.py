import VRScript
import level
import math
import random
# ------------------------ Player ------------------------ #

healthWarn_1 = VRScript.Core.Audible('healthWarn_1', 'Sound Effects/warning/fvox/health_dropping.wav')
healthWarn_2 = VRScript.Core.Audible('healthWarn_2', 'Sound Effects/warning/fvox/health_dropping2.wav')
healthWarn_3 = VRScript.Core.Audible('healthWarn_3', 'Sound Effects/warning/fvox/internal_bleeding.wav')
healthWarn_4 = VRScript.Core.Audible('healthWarn_4', 'Sound Effects/warning/fvox/near_death.wav')

footstep = VRScript.Core.Audible('footstep', 'Sound Effects/footsteps/hardboot_generic1.wav')


userMat = VRScript.Math.Matrix()
hpStat = VRScript.Core.FontText('playerHP', "100")
red = VRScript.Core.Color(1, 0, 0, 0.6)
yellow = VRScript.Core.Color(1, 1, 0, 0.6)
brown = VRScript.Core.Color(1, 0.7, 0, 0.6)
orange = VRScript.Core.Color(1, 0.5, 0, 0.6)
reddish = VRScript.Core.Color(1, 0.3, 0, 0.6)

class Player():
    def __init__(self, name=""):
        self.OnInit(name)

    def OnInit(self, info):
        # Set the player's HP to 100 and Armor to 0 by default
        self.hp = 100
        self.armor = 0
        self.isWarned = False
        self.pent = VRScript.Core.Entity(info)
        
        #physProps = VRScript.Core.PhysicsProperties(0, 0.4, 0.3, 0.3, 0.5)
    ##                self.mesh = VRScript.Resources.Mesh(self.getName(), self.filename, mat)
        size = .3
        #phys = VRScript.Core.Physical(info, VRScript.Resources.Box(VRScript.Math.Vector(-size,-size,-size), VRScript.Math.Point(1.4,-2,-2)))
    ##                phys = VRScript.Core.Physical(self.getName())
        #self.attach(phys)
        #self.physical('').setPhysicsProperties(physProps)
        #self.physical('').setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
        #self.physical('').setCollisionType(VRScript.Core.CollisionType.Kinematic)
        #self.physical('').setProximity(True)
        #phys.enableDebugVisual(True)

    
    def showHUD(self):
        hpStat.setColor(yellow)
        hpStat.show()
        self.pent.attach(hpStat)
        self.pent.movable().setParent('User0')
        hudPos = VRScript.Math.Matrix()
        hudPos.preTranslation(VRScript.Math.Vector(-1,1,2))
        self.pent.movable().setPose(hudPos)
        
    def OnUpdate(self, info):
    ##                print("Player HP: " + str(self.hp))
        hpStat.setText(str(self.hp))
        if(self.hp < 75 and self.hp > 50):
                hpStat.setColor(brown)
                if(self.isWarned == False):
                        healthWarn_1.play()
                        self.isWarned = True
        elif(self.hp <= 50 and self.hp > 35):
                hpStat.setColor(orange)
                if(self.isWarned == True):
                        healthWarn_2.play()
                        self.isWarned = False
        elif(self.hp <= 35 and self.hp > 20):
                hpStat.setColor(reddish)
                if(self.isWarned == False):
                        healthWarn_3.play()
                        self.isWarned = True
        elif(self.hp <= 20):
                hpStat.setColor(red)
                if(self.isWarned == True):
                        healthWarn_4.play()
                        self.isWarned = False
                        

# ------------------------ Enemy ------------------------ #

Ouch = VRScript.Core.Audible('Ouch', 'Sound Effects/Pain Voices/voices/ba_pain08.wav')
Hurt = VRScript.Core.Audible('Hurt', 'Sound Effects/antlion/pain2.wav')
Hit = VRScript.Core.Audible('Hit', 'Sound Effects/antlion/shell_strike4.wav')
Die = VRScript.Core.Audible('Die', 'Sound Effects/antlion/digdown.wav')
Idle = VRScript.Core.Audible('Ant_idle', 'Sound Effects/antlion/idle2.wav')
Antlion_Angry = VRScript.Core.Audible('Ant_Angry', 'Sound Effects/antlion_guard/angry3.wav')
Antlion_Attack = VRScript.Core.Audible('Ant_Attack', 'Sound Effects/antlion/attack_single1.wav')

class Enemy():
        Z_OFFSET = .8
        pos = [0,0]
        dest = [0,0]
        DELAY = 20
        timer = 0
        MAX_HP = 5
        hp = 0
        moving = False
        dying = False

        def __init__(self, enum):
                self.enum = enum

        def load(self, filename, size):
                self.filename = filename
                print("Load animation: ")
                print(self.filename)
                self.eent = VRScript.Core.Entity("enemy"+self.enum);
                mat = VRScript.Math.Matrix()
                mat.preScale(VRScript.Math.Vector(size, size, size))
                mat.preAxisAngle(90,VRScript.Math.Vector(1,0,0))
                mat.postTranslation(VRScript.Math.Vector(-0,-20,0))
                
                self.eent.mesh = VRScript.Resources.Mesh(self.eent.getName(), self.filename, mat)
                self.eent.attach(VRScript.Core.Renderable(self.eent.getName(), self.eent.mesh))
                self.eent.renderable('').show()
                self.eent.attach(VRScript.Core.Animable(self.eent.getName(), self.eent.mesh))

                self.state = 0
                self.type = "enemy"

                
        def OnInit(self, info):
                pass

        def OnUpdate(self, info, player, user, facing):
            #progress delay, update position
            self.timer += 1
            if self.dying and self.timer < self.DELAY:
                imat = VRScript.Math.Matrix()
                z = self.Z_OFFSET  - (self.timer/self.DELAY)
                imat.preTranslation(VRScript.Math.Vector(self.pos[0], self.pos[1], z))
                self.eent.movable().setPose(imat)
                return
            elif self.dying :
                self.level.mobAlive = False
                self.eent.renderable('').hide()
                self.dying = False
                return

            if self.timer < self.DELAY : 
                if self.moving:
                    imat = VRScript.Math.Matrix()
                    x = self.pos[0] + ((self.dest[0] - self.pos[0]) * (self.timer/self.DELAY))
                    y = self.pos[1] + ((self.dest[1] - self.pos[1]) * (self.timer/self.DELAY))
                    #figure out rotate
                    #angle = -math.degrees(math.acos(VRScript.Math.Vector(0,1,0).dot(VRScript.Math.Vector(self.dest[0]-self.pos[0], self.dest[1]-self.pos[1],0))))
                    angle = math.degrees(math.atan2(self.dest[0] - self.pos[0], -(self.dest[1] - self.pos[1])))
                    imat.preAxisAngle(angle, VRScript.Math.Vector(0,0,1))
                    imat.preTranslation(VRScript.Math.Vector(x*3, y*3, self.Z_OFFSET))
                    self.eent.movable().setPose(imat)
                return
            if self.timer == self.DELAY : 
                if self.moving:
                    imat = VRScript.Math.Matrix()
                    x = self.pos[0] + ((self.dest[0] - self.pos[0]) * (self.timer/self.DELAY))
                    y = self.pos[1] + ((self.dest[1] - self.pos[1]) * (self.timer/self.DELAY))
                    #figure out rotate
                    #angle = -math.degrees(math.acos(VRScript.Math.Vector(0,1,0).dot(VRScript.Math.Vector(self.dest[0]-self.pos[0], self.dest[1]-self.pos[1],0))))
                    angle = math.degrees(math.atan2(user[0] - self.dest[0], -(user[1] - self.dest[1])))
                    imat.preAxisAngle(angle, VRScript.Math.Vector(0,0,1))
                    imat.preTranslation(VRScript.Math.Vector(x*3, y*3, self.Z_OFFSET))
                    self.eent.movable().setPose(imat)
                return

            # delay over, update
            if self.moving:
                self.pos[0] = self.dest[0]
                self.pos[1] = self.dest[1]
                self.moving = False

            self.timer = 0
            
            # Update behavior when weapon is in contact with it
            # Move closer to user when approaching enemy
            xDist = user[0] - self.pos[0]
            yDist = user[1] - self.pos[1]
            
            # next to
            if (abs(xDist) <= 1 and abs(yDist) <= 1):
                imat = VRScript.Math.Matrix()
                angle = math.degrees(math.atan2(user[0] - self.dest[0], -(user[1] - self.dest[1])))
                imat.preAxisAngle(angle, VRScript.Math.Vector(0,0,1))
                imat.preTranslation(VRScript.Math.Vector(self.pos[0]*3, self.pos[1]*3, .3))
                self.eent.movable().setPose(imat)
                self.state = 2
                player.hp = player.hp - 1
                if facing == 0: # forward
                    if self.pos[1] > user[1]:
                        self.hp -= 1
                        Hurt.play()
                        Hit.play()
                elif facing == 1: # right
                    if self.pos[0] > user[0]:
                        self.hp -= 1
                        Hurt.play()
                        Hit.play()
                elif facing == 2: # back 
                    if self.pos[1] < user[1]:
                        self.hp -= 1
                        Hurt.play()
                        Hit.play()
                elif facing == 3: # left
                    if self.pos[0] < user[0]:
                        self.hp -= 1
                        Hurt.play()
                        Hit.play()
                        

                # moving towards
            elif (abs(xDist) + abs(yDist)) < 8:
                self.state = 1
                if abs(xDist) > 1 :
                    if xDist > 0 :
                        if self.level.isPassable(self.pos[0] + 1, self.pos[1]):
                            self.dest[0] = self.pos[0] + 1
                    else:
                        if self.level.isPassable(self.pos[0] - 1, self.pos[1]):
                            self.dest[0] = self.pos[0] - 1

                if abs(yDist) > 1 :
                    if yDist > 0 :
                        if self.level.isPassable(self.pos[0], self.pos[1] + 1):
                            self.dest[1] = self.pos[1] + 1
                    else:
                        if self.level.isPassable(self.pos[0], self.pos[1] - 1):
                            self.dest[1] = self.pos[1] - 1

                self.moving = True

            else:
                self.state = 0
                
            if self.hp <= 0:
                Die.play()
                self.dying = True

            else: 
                self.applyState()
                

        def applyState(self):
            if(self.state == 0):
                if random.random() < .25 :
                    Idle.play()
            elif(self.state == 1):
                Antlion_Angry.play()
            elif(self.state == 2):
                Ouch.play()
                Antlion_Attack.play()
                
        def play(self, mode):
                self.eent.anim = VRScript.Core.AnimationStrip('Take 001', 0.0, 0.0, 0, mode)
                self.eent.animable('').play(self.eent.anim)

        def stop(self):
                self.eent.animable('').stop()

        def getProperties(self):
                return self.type

        def isHere(self, x, y):
            if self.moving:
                return self.dest[0] == x and self.dest[1] == y
            else:
                return self.pos[0] == x and self.pos[1] == y

        def spawnLoc(self, enemyName, filename, x, y, size, level):
                imat = VRScript.Math.Matrix()
                self.load(filename, size)
                self.play(VRScript.Core.PlayMode.Loop);
                imat.preTranslation(VRScript.Math.Vector(x*3, y*3, self.Z_OFFSET))
                self.pos = [x,y]
                self.dest = [x,y]
                self.eent.movable().setPose(imat)
                self.level = level
                self.timer = 0
                self.hp = self.MAX_HP
