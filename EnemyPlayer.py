import VRScript
import level
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

class Player(VRScript.Core.Behavior):
        def __init__(self, entity=None):
                VRScript.Core.Behavior.__init__(self,entity)

        def OnInit(self, info):
                # Set the player's HP to 100 and Armor to 0 by default
                self.hp = 100
                self.armor = 0
                self.isWarned = False
                
                physProps = VRScript.Core.PhysicsProperties(0, 0.4, 0.3, 0.3, 0.5)
##                self.mesh = VRScript.Resources.Mesh(self.getName(), self.filename, mat)
                size = .3
                phys = VRScript.Core.Physical(self.getName(), VRScript.Resources.Box(VRScript.Math.Vector(-size,-size,-size), VRScript.Math.Point(1.4,-2,-2)))
##                phys = VRScript.Core.Physical(self.getName())
                self.attach(phys)
                self.physical('').setPhysicsProperties(physProps)
                self.physical('').setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
                self.physical('').setCollisionType(VRScript.Core.CollisionType.Kinematic)
                self.physical('').setProximity(True)
                phys.enableDebugVisual(True)

                
        def showHUD(self):
                hpStat.setColor(yellow)
                hpStat.show()
                self.attach(hpStat)
                self.movable().setParent('User0')
                hudPos = VRScript.Math.Matrix()
                hudPos.preTranslation(VRScript.Math.Vector(-1,1,2))
                self.movable().setPose(hudPos)
                
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
                        
player = Player("Player")
player.showHUD()

# ------------------------ Enemy ------------------------ #

Ouch = VRScript.Core.Audible('Ouch', 'Sound Effects/Pain Voices/voices/ba_pain08.wav')
##Antlion_Idle = VRScript.Core.Audible('Ant_idle', 'Sound Effects/antlion/idle2.wav')
##loop = Antlion_Idle.getAudioProperties()
##loop.loop = True
##Antlion_Idle.setAudioProperties(loop)
Antlion_Angry = VRScript.Core.Audible('Ant_Angry', 'Sound Effects/antlion_guard/angry3.wav')
Antlion_Attack = VRScript.Core.Audible('Ant_Attack', 'Sound Effects/antlion/attack_single1.wav')

class Enemy(VRScript.Core.Behavior):
        pos = [0,0]
        DELAY = 20
        timer = 0

        def __init__(self, entity=None):
                VRScript.Core.Behavior.__init__(self,entity)

                
        def load(self, filename, size):
                self.filename = filename
                print("Load animation: ")
                print(self.filename)
                mat = VRScript.Math.Matrix()
                mat.preScale(VRScript.Math.Vector(size, size, size))
                mat.preAxisAngle(90,VRScript.Math.Vector(1,0,0))
                mat.postTranslation(VRScript.Math.Vector(-0,-20,0))
                
                self.mesh = VRScript.Resources.Mesh(self.getName(), self.filename, mat)
                self.attach(VRScript.Core.Renderable(self.getName(), self.mesh))
                self.renderable('').show()
                self.attach(VRScript.Core.Animable(self.getName(), self.mesh))

                self.state = 0  # State of the enemy: 0 for idle, 1 for alert, 2 for attack, 3 for under attack, 4 for dying
                self.type = "enemy"

                
        def OnInit(self, info):
                pass

        def OnUpdate(self, info):
                self.timer -= 1
                if self.timer != 0 : return
                self.timer = self.DELAY
                print("MONSTAR")
                print(self.pos)

                # Update behavior when weapon is in contact with it
                # Move closer to user when approaching enemy
                user0 = VRScript.Core.Entity('User0')
                userWorldPos = user0.movable().selfToWorld().getTranslation()
                userGridPos = [int(userWorldPos.x/3), int(userWorldPos.y/3)]

                print("YOU")
                print(userGridPos)

                xDist = userGridPos[0] - self.pos[0]
                yDist = userGridPos[1] - self.pos[1]

                # next to
                if (abs(xDist) <= 1 and abs(yDist) <= 1):
                        self.state = 2
#                        if(info.frameTime%1 > 0.99):                                        
                        player.hp = player.hp - 1
                        Ouch.play()

                # moving towards
                elif (abs(xDist) + abs(yDist)) < 4:
                        self.state = 1
                        if abs(xDist) > abs(yDist):
                                if xDist > 0 :
                                        self.pos[0] = self.pos[0] + 1
                                else:
                                        self.pos[0] = self.pos[0] - 1
                        else:
                                if yDist > 0 :
                                        self.pos[1] = self.pos[1] + 1
                                else:
                                        self.pos[1] = self.pos[1] - 1
                                print(self.pos)
                else:
                        self.state = 0

                self.applyState()


        def applyState(self):
                if(self.state == 0):
                        Antlion_Idle = VRScript.Core.Audible(self.getName()+'Ant_idle', 'Sound Effects/antlion/idle2.wav')
                        loop = Antlion_Idle.getAudioProperties()
                        loop.loop = True
                        self.attach(Antlion_Idle)
                        self.audible(self.getName()+'Ant_idle').play()
                elif(self.state == 1):
                        Antlion_Angry.play()
                elif(self.state == 2):
                        Antlion_Attack.play()
                        
        def play(self, mode):
                self.anim = VRScript.Core.AnimationStrip('Take 001', 0.0, 0.0, 0, mode)
                self.animable('').play(self.anim)

        def stop(self):
                self.animable('').stop()

        def getProperties(self):
                return self.type


        def spawnLoc(self, enemyName, filename, x, y, size, level):
                imat = VRScript.Math.Matrix()
                enemy = Enemy(enemyName)
                enemy.load(filename, size)
                enemy.play(VRScript.Core.PlayMode.Loop);
                imat.preTranslation(VRScript.Math.Vector(x*3, y*3, 0))
                self.pos = [x,y]
                enemy.movable().setPose(imat)
                self.level = level
                self.timer = self.DELAY
