from FSMs.screen import ScreenManagerFSM
#from . import TextEntry, EventMenu
#from vector import *
from constants import *
from gameManager import GameManager
from vector import *
from pygame.locals import *
from text import TextEntry
from menu import *

class ScreenManager(object):
      
    def __init__(self):
        self.game =  GameManager()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        
        size = self.pausedText.getSize()
        midpoint = UPSCALED // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("background.jpeg", fontName="default8")
        self.mainMenu.addOption("start", "Press 1 to start Game",
                                 UPSCALED // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        self.mainMenu.addOption("exit", "Press 2 to exit Game",
                                 UPSCALED // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        
        self.statsMenu = StatsMenu("stats.jpeg", fontName="default8")
        #self.statsMenu.addStat("Speed", "2", UPSCALED // 2 - vec(0,50), center=None)
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        elif self.state == "inStats":
            self.statsMenu.draw(drawSurf)
    
    
    def handleEvent(self, event, seconds):
        #print(self.state)
        if event.type == KEYDOWN and event.key == K_s:
            self.state.stats()
        elif self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.game.handleEvent(event, seconds)
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
        elif self.state == "inStats":
            self.statsMenu.handleEvent(event)
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
        elif self.state == "inStats":
            self.statsMenu.update(seconds)
            self.update_game_stats()

    def update_game_stats(self):
        """Update game stats based on changes in the stats menu."""
        spread_stat_value = self.statsMenu.stats.get("Spread", 0)
        speed_stat_value = self.statsMenu.stats.get("Speed", 0)
        self.game.randomness = 100000 / (2 * speed_stat_value)
        new_modifier = self.calculate_modifier(spread_stat_value)
        self.game.update_spread_rate(new_modifier)

    def calculate_modifier(self, stat_value):
        """Calculate modifier from stat value. Adjust this based on your game's logic."""
        return 1.0 + (stat_value * 100)