from FSMs.screen import ScreenManagerFSM
#from . import TextEntry, EventMenu
#from vector import *
from constants import *
from gameManager import GameManager
from vector import *
from pygame.locals import *
from text import TextEntry
from menu import *
import requests
import random 
from PIL import Image
from io import BytesIO
import threading
from AI import runAI
import time
import os
from dotenv import load_dotenv
from soundManager import SoundManager

load_dotenv()
API_KEY = os.getenv("HF")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

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
        self.winMenu = WinMenu("overlay.jpeg", fontName="TITLE")
        self.loseMenu = LoseMenu("background.jpeg", fontName="TITLE")
        self.event_lock = threading.Lock()
        self.event_processing = False
        self.soundManager = SoundManager()
        #self.eventMenu = EventMenu("astronaut_horse.png", fontName="default8")      
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        elif self.state == "inStats":
            self.statsMenu.draw(drawSurf)
        elif self.state == "winMenu":
            self.winMenu.draw(drawSurf)
        elif self.state == "loseMenu":
            self.loseMenu.draw(drawSurf)
        elif self.state == "eventMenu":
            self.eventMenu.draw(drawSurf)
    
    def generate_image(self, prompt):
        timestamp = int(time.time())
        new_image_path = f"images/event_{timestamp}.png"

        old_image_path = getattr(self, 'last_image_path', None)
        
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {
            "inputs": prompt,
            "options": {
                "wait_for_model": True,
            },
        }

        with requests.post(API_URL, headers=headers, json=payload) as response:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            resized_image = image.resize((int(UPSCALED[0]), int(UPSCALED[1])))
            resized_image.save(new_image_path)

        if old_image_path and os.path.exists(old_image_path) and old_image_path != new_image_path:
            os.remove(old_image_path)
        self.last_image_path = new_image_path

        return new_image_path

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
        elif self.state == "eventMenu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 650 <= mouse_pos[0] <= 700 and 50 <= mouse_pos[1] <= 100:
                    self.state.event()

    def process_random_event(self):
        title, description = runAI()
        new_image_path = self.generate_image(description)
        filename = os.path.basename(new_image_path)
        self.eventMenu = RandomMenu(filename, fontName="default8")    
        self.eventMenu.addInformation(title, description)
        self.state.event()
        self.statsMenu.totalPoints += 1
        self.statsMenu.editOption("Total Points", f"Total Points: {self.statsMenu.totalPoints}")
        self.soundManager.getInstance().playSFX("robot.wav")
        with self.event_lock:
            self.event_processing = False
    
    def update(self, seconds):
        if self.state == "game":
            if self.game.isWin():
                self.state.winGame()
            elif self.game.isLose():
                self.state.loseGame()
            elif random.randint(0, 300) <= self.statsMenu.stats.get("Research", 0) and not self.event_processing:
                with self.event_lock:
                    if not self.event_processing:
                        self.event_processing = True
                        thread = threading.Thread(target=self.process_random_event)
                        thread.start()
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
        elif self.state == "inStats":
            self.statsMenu.update(seconds)
            self.update_game_stats()

    def update_game_stats(self):
        spread_stat_value = self.statsMenu.stats.get("Speed", 0)
        speed_stat_value = self.statsMenu.stats.get("Spreed", 0)
        bar_stat_value = self.statsMenu.stats.get("Cyber Security", 0)

        self.game.randomness =  100000 / (2 * speed_stat_value) if speed_stat_value != 0 else 100000
        new_modifier = self.calculate_modifier(spread_stat_value)
        self.game.update_spread_rate(new_modifier)
        self.game.update_bar(bar_stat_value)

    def calculate_modifier(self, stat_value):
        return 1.0 + (stat_value * 100)