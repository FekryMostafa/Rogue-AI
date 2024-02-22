import pygame
import pygame.gfxdraw
from mobile import Drawable
import vector as v
from constants import WORLDSIZE
import random


class Server(Drawable): 
    def __init__(self, imageName, offset, position):
        super().__init__(imageName, offset, position)
        self.infection_radius = 0
        self.infected = False

    def infect(self):
        self.infected = True
        self.infection_radius = 50

    def update(self, seconds):
        if self.infected:
            self.infection_radius += 0.1
    
    def draw(self, surface, overlay):
        super().draw(surface)
        print()
        if self.infected:
            infection_color = (0, 0, 0, 0)
            pygame.gfxdraw.filled_circle(overlay, int(self.position[0] + 0.5 * self.getSize()[0]), int(self.position[1] + 0.5 * self.getSize()[1]), int(self.infection_radius), infection_color)

