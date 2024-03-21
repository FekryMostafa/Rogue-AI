import pygame
import vector as v
from drawable import Drawable
from constants import *
from random import choice, randrange
from server import Server

class GameManager(object):
    def __init__(self):
        self.score = 0
        self.background = Drawable("background.jpeg", None, (0, 0))
        #self.overlay = Drawable("overlay.jpeg", None, (0,0))
        self.overlay = pygame.image.load("images/overlay.jpeg").convert_alpha()
        self.drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
        self.servers = {}

        self.serverPositions = [
            (100, 100), (200, 200), (300, 300), (870, 300), (800, 500), (830, 600), (1380, 570), (1275, 444), (740, 400), (1000, 180), (1300, 150), (1150, 200), (1105, 340), (1015, 278), (755, 200), (400, 460), (360, 690), (510, 480)
            ]
        self.connections = {
            0: [1, 5],
            1: [2, 4],
            2: [3, 6],
            3: [7, 10],
            4: [8, 5],
            5: [9],
            6: [11, 14],
            7: [12],
            8: [13],
            9: [14],
            10: [15],
            11: [16],
            12: [17],
            13: [15],
            14: [16],
            15: [17],
            16: [0],
            17: [1]
            }
        for i, position in enumerate(self.serverPositions):
            self.servers[f"server{i}"] = Server("server.png", None, position)
        self.server_keys = list(self.servers.keys())
        self.random_server_key = self.server_keys[randrange(len(self.server_keys))]
        self.servers[self.random_server_key].infect()
        self.spread_rate_modifier = 1.0
        self.randomness = 100000
    
    def update(self, seconds):
        for server_id, server in self.servers.items():
            server.update(seconds)
        if randrange(self.randomness) == 23:
            random_server_key = choice(list(self.connections.keys()))
            random_connected_server_index = choice(self.connections[random_server_key])
            random_connected_server_key = f"server{random_connected_server_index}"
            self.servers[random_connected_server_key].infect()

    def update_spread_rate(self, new_modifier):
        """Update the infection spread rate based on game stats."""
        self.spread_rate_modifier = new_modifier
        for server in self.servers.values():
            server.infection_speed = 0.0001 * self.spread_rate_modifier

    def handleEvent(self, event, seconds):
        pass
    
    def draw(self, screen):
        self.drawSurface.fill((255, 255, 255))
        self.background.draw(self.drawSurface)   
        self.drawSurface.blit(self.overlay, (0, 0))
        for server_id, server in self.servers.items():
            server.draw(self.drawSurface, self.overlay)

        for server, connected_servers in self.connections.items():
            for connected_server in connected_servers:
                pygame.draw.line(self.drawSurface, (255, 255, 255, 50), self.serverPositions[server], self.serverPositions[connected_server], 1)

        pygame.transform.scale(self.drawSurface, UPSCALED, screen)
