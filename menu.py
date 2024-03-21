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

    def editOption(self, key, new_text):
        if key in self.options:
            self.options[key].update_text(new_text)  # Use the new method to update text
        else:
            raise KeyError(f"Key '{key}' not found in options.")
        
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
        self.positions = [
            (350, 160),
            (350, 210),
            (350, 260),
            (350, 310)
        ]
        self.totalPoints = 10

        self.initialize_stats()

        self.button_positions = {
            "Spread": [(200, 150), (450, 150)],
            "Speed": [(200, 200), (450, 200)],
            "Research": [(200, 250), (450, 250)],
            "Cyber Security": [(200, 300), (450, 300)]
        }

    def addStat(self, key, initialValue, position, center=None):
        super().addOption(key, f"{key}: {initialValue}", position, center)
        self.stats[key] = initialValue

    def initialize_stats(self):
        self.addStat("Spread", 0, self.positions[0], "horizontal")
        self.addStat("Speed", 0, self.positions[1], "horizontal")
        self.addStat("Research", 0, self.positions[2], "horizontal")
        self.addStat("Cyber Security", 0, self.positions[3], "horizontal")
        self.addOption("Total Points", f"Total Points: {self.totalPoints}", (600, 20), "horizontal")

    def draw(self, surface):
        super().draw(surface)

        for key, button_positions in self.button_positions.items():
            up_button, down_button = button_positions
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(up_button[0], up_button[1], 50, 30))
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(down_button[0], down_button[1], 50, 30))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for key, button_positions in self.button_positions.items():
                down_button, up_button = [pygame.Rect(x, y, 50, 30) for x, y in button_positions]
                if up_button.collidepoint(mouse_pos):
                    if self.totalPoints > 0:
                        self.stats[key] += 1
                        self.totalPoints -= 1

                        self.editOption(key, f"{key}: {self.stats[key]}")
                    #print(self.options[key].text)
                elif down_button.collidepoint(mouse_pos):
                    if self.stats[key] > 0:
                        self.stats[key] -= 1
                        self.totalPoints += 1
                        self.editOption(key, f"{key}: {max(self.stats[key], 0)}")
            self.editOption("Total Points", f"Total Points: {self.totalPoints}") 