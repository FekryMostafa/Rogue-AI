from FSMs.screen import ScreenManagerFSM
#from . import TextEntry, EventMenu
#from vector import *
from constants import *
from gameManager import GameManager
from vector import *
from pygame.locals import *
from text import TextEntry
from menu import EventMenu

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
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
    
    
    def handleEvent(self, event, seconds):
        if self.state in ["game", "paused"]:
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
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
    