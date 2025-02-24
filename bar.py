import pygame
import pygame.gfxdraw
from mobile import Drawable
import vector as v
from constants import WORLDSIZE

class Bar(Drawable):
    def __init__(self, imageName, offset, position):
        super().__init__(imageName, offset, position)
        self.progress = 0
        self.bar_width = 200
        self.bar_height = 20
        self.bar_color = (0, 0, 255)
        self.barPosition = position + v.vec(65, 25)
        self.modifier = 1.0

    def adjustModifier(self, modifier):
        self.modifier = modifier + 1.0
        #print(self.modifier)

    def update(self, seconds):
        if self.progress < 100:
            self.progress += 0.01 / self.modifier

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.rect(surface, (255, 255, 255), (self.barPosition[0], self.barPosition[1], self.bar_width, self.bar_height))
        
        filled_width = int((self.progress / 100) * self.bar_width)
        
        pygame.draw.rect(surface, self.bar_color, (self.barPosition[0], self.barPosition[1], filled_width, self.bar_height))
        
        pygame.draw.rect(surface, (0, 0, 0), (self.barPosition[0], self.barPosition[1], self.bar_width, self.bar_height), 2)