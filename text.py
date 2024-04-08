from drawable import Drawable
import pygame
import os

class TextEntry(Drawable):   
    if not pygame.font.get_init():
        pygame.font.init()
    
    FONT_FOLDER = "fonts" 
    DEFAULT_FONT = "PressStart2P.ttf"
    DEFAULT_SIZE = 16   
    FONTS = {
       "default" : pygame.font.Font(os.path.join(FONT_FOLDER,
                                    DEFAULT_FONT), DEFAULT_SIZE),
       "default8" : pygame.font.Font(os.path.join(FONT_FOLDER,
                                    DEFAULT_FONT), 8),
        "TITLE": pygame.font.Font(os.path.join(FONT_FOLDER,
                                    DEFAULT_FONT), 60)
    }
  
    def __init__(self, position, text, font="default",
              color=(255,255,255)):
        super().__init__(position=position, imageName="")
        self.color = color
        self.text = text
        self.font = font 
        self.render_text()
    
    def render_text(self):
        """Render the text to the image surface."""
        self.image = TextEntry.FONTS[self.font].render(self.text, False, self.color)
        
    def update_text(self, new_text):
        """Update the text and re-render it."""
        if new_text != self.text:
            self.text = new_text
            self.render_text()