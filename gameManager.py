import pygame
import vector as v
from drawable import Drawable
from constants import *
from random import randrange
from server import Server

class GameManager(object):
    def __init__(self):
        self.score = 0
        self.background = Drawable("background.jpeg", None, (0, 0))
        #self.overlay = Drawable("overlay.jpeg", None, (0,0))
        self.overlay = pygame.image.load("images/overlay.jpeg").convert_alpha()
        self.drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
        self.servers = {}

        serverPositions = [(100, 100), (200, 200), (300, 300), (870, 300), (800, 500), (830, 600), (1380, 570), (1275, 444), (740, 400), (1000, 180), (1300, 150), (1150, 200), (1105, 340), (1015, 278), (755, 200), (400, 460), (360, 690), (510, 480)]
        for i, position in enumerate(serverPositions):
            self.servers[f"server{i}"] = Server("server.png", None, position)
        self.server_keys = list(self.servers.keys())
        self.random_server_key = self.server_keys[randrange(len(self.server_keys))]
        self.servers[self.random_server_key].infect()

    def update(self, seconds):
        for server_id, server in self.servers.items():
            server.update(seconds)
        if randrange(10000) == 23:
            print("success")
            random_server_key = self.server_keys[randrange(len(self.server_keys))]
            self.servers[random_server_key].infect()

    def handleEvent(self, event, seconds):
        pass
    
    def draw(self, screen):
        self.drawSurface.fill((255, 255, 255))
        self.background.draw(self.drawSurface)   
        self.drawSurface.blit(self.overlay, (0, 0))
        for server_id, server in self.servers.items():
            server.draw(self.drawSurface, self.overlay)
        pygame.transform.scale(self.drawSurface, UPSCALED, screen)
