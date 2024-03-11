import vector as v
from spriteManager import SpriteManager

class Drawable(object):
   camera_offset = v.vec(0, 0)

   def __init__(self, imageName="", offset=None, position=v.vec(0,0)):
      if imageName != "":
         self.image = SpriteManager.getInstance().getSprite(imageName, offset)
      self.position = v.vec(*position)
      self.imageName = imageName


   def draw(self, surface):
      surface.blit(self.image, (self.position[0], self.position[1]))
    
   def setPosition(self, newPosition):
      self.position = newPosition
   
   def getPosition(self):
      return self.position

   def getImage(self):
      return self.image

   def getRect(self):
      return self.image.get_rect()
   
   def getSize(self):
        return v.vec(*self.image.get_size())

   def update(self, seconds):
      pass