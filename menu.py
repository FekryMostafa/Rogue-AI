from drawable import Drawable
from vector import vec, magnitude
from text import TextEntry

import pygame

class AbstractMenu(Drawable):
    def __init__(self, background, fontName="default",
                 color=(255,255,255)):
        super().__init__(background, None, (0 ,0))
           
        self.options = {}
        
        self.color = color      
        self.font = fontName
     
    def addOption(self, key, text, position, center=None):
        self.options[key] = TextEntry(position, text, self.font,
                                  self.color)
        optionSize = self.options[key].getSize()
        
        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)
            
            self.options[key].position -= offset
 
    def draw(self, surface):
        super().draw(surface)
        
        for item in self.options.values():
           item.draw(surface)


class EventMenu(AbstractMenu):
    def __init__(self, background, fontName="default",
                color=(255,255,255)):
        super().__init__(background, fontName, color)      
        self.eventMap = {}
     
    def addOption(self, key, text, position, eventLambda,
                                              center=None):
        super().addOption(key, text, position, center)      
        self.eventMap[key] = eventLambda
    
    def handleEvent(self, event):      
        for key in self.eventMap.keys():
            function = self.eventMap[key]
            if function(event):
                return key

class StatsMenu(AbstractMenu):
    def __init__(self, background, fontName="default", color=(255,255,255)):
        super().__init__(background, fontName, color)
        self.stats = {}

    def addStat(self, key, initialValue, position, center=None):
        super().addOption(key, f"{key}: {initialValue}", position, center)
        self.stats[key] = initialValue

    def updateStat(self, key, value):
        self.stats[key] = str(value)
        self.options[key].setText(f"{key}: {value}")

    def draw(self, surface):
        super().draw(surface)
        
    
    
        
        

