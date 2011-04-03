import VRScript

import Skel


R2D = 57.29578 
Magic = 6


floor = VRScript.Core.Entity('Floor')
#mat = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(10,10,10)).postTranslation(VRScript.Math.Vector(0,0,-10))
fbox=VRScript.Resources.Box(VRScript.Math.Vector(1,1,1)*10, VRScript.Math.Point(0,0,-10))
floor.attach(VRScript.Core.Renderable('Floor',fbox))
floor.renderable('').show()

phys = VRScript.Core.Physical('Floor', fbox)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.1,.1,.1,.2))
phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
floor.attach(phys)




ball = VRScript.Core.Entity('ball')
sph = VRScript.Resources.Sphere(.25)
ball.attach(VRScript.Core.Renderable("ball",sph))
ball.renderable('').show()

phys = VRScript.Core.Physical('ball', sph)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(1,.1,.1,.1,.2))
phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
ball.attach(phys)

mat = VRScript.Math.Matrix().postTranslation(VRScript.Math.Vector(0,-2,1))
ball.movable().setPose(mat)



ball1 = VRScript.Core.Entity('ball1')
sph = VRScript.Resources.Sphere(.25)
ball1.attach(VRScript.Core.Renderable("ball1",sph))
ball1.renderable('').show()

phys = VRScript.Core.Physical('ball1', sph)
phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(1,.1,.1,.1,.2))
phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
ball1.attach(phys)

mat = VRScript.Math.Matrix().postTranslation(VRScript.Math.Vector(1,-1,1))
ball1.movable().setPose(mat)





class marker(VRScript.Core.Behavior):
	def __init__(self,entity=None):
		VRScript.Core.Behavior.__init__(self,entity)
		self._bone = -1

		sph = VRScript.Resources.Sphere(0.1)
		self.attach(VRScript.Core.Renderable(self.getName(),sph))
		#self.attach(VRScript.Core.Renderable(self.getName(),VRScript.Resources.Mesh(self.getName(),"bone.obj")))
		self.renderable(self.getName()).show()

#		phys = VRScript.Core.Physical(self.getName(), sph)
#		phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(100.01,.1,.1,.1,.2))
#		phys.setConstraints(VRScript.Math.Vector(1,1,1), VRScript.Math.Vector(1,1,1))
#		phys.setCollisionType(VRScript.Core.CollisionType.Dynamic)
#		self.attach(phys)


#	def OnInit(self, info):
		#self.attach(VRScript.Core.Renderable(self.getName(),VRScript.Resources.Sphere(0.1)))


	def OnUpdate(self, info):
		if (self._bone >= 0):
			v = VRScript.Math.Vector(Skel.getPosX(self._bone),Skel.getPosY(self._bone),Skel.getPosZ(self._bone))
			q = VRScript.Math.Quat(Skel.getQuatX(self._bone),Skel.getQuatY(self._bone),Skel.getQuatZ(self._bone),Skel.getQuatW(self._bone))
			mat = VRScript.Math.Matrix()
			#mat.preAxisAngle(90,VRScript.Math.Vector(1,0,0))
			#mat.preAxisAngle(90,VRScript.Math.Vector(1,0,0))
			mat.preQuat(q)
			mat.preTranslation(v)
			# Orient up
			mat.preAxisAngle(90,VRScript.Math.Vector(1,0,0))
			# Move
			mat.preTranslation(VRScript.Math.Vector(0,5,2))
			self.movable().setPose(mat)
			# Show the magic bone #
			if (self._bone==Magic):
				e = (VRScript.Math.Matrix().preQuat(q)).getEuler()
				print("Roll: " + str(e.x) + "\tPitch: " + str(e.y) + "\tYaw: " + str(e.z))
				#print(str(Skel.getQuatX(self._bone))+","+str(Skel.getQuatY(self._bone))+","+str(Skel.getQuatZ(self._bone))+","+str(Skel.getQuatW(self._bone)))

	def setBone(self, bone):
		self._bone = bone
		if (bone==Magic):
			mp = self.renderable('').getMaterialProperties()
			mp.wireframe = True
			self.renderable(self.getName()).setMaterialProperties(mp)


Skel.start()

skeleton = list();


#bones = {7,8,9}
#for i in bones:

i=0
while i<24:
	m = marker("m"+str(i))
	m.setBone(i)
	skeleton.append(m)
	i=i+1

#Skel.stop()

