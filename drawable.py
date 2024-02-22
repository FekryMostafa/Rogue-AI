import vector as v
from spriteManager import SpriteManager

class Drawable(object):
   camera_offset = v.vec(0, 0)

   def __init__(self, imageName, offset, position):
        SM = SpriteManager.getInstance()        
        self.position = v.vec(*position)
        self.image = SM.getSprite(imageName, offset)


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
      return self.image.get_size()