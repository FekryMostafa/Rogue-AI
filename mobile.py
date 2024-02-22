from drawable import Drawable
import vector as v

class Mobile(Drawable):
   def __init__(self, imageName, offset, position):
      super().__init__(imageName, offset, position)
      self.velocity = v.vec(0,0)
   
   def update(self, seconds):
      self.position += self.velocity * seconds

   def setVelocity(self, velocity):
      self.velocity = velocity