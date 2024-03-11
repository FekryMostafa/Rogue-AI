import pygame
from screenManager import ScreenManager
from constants import UPSCALED

def main():
    pygame.init()
    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    game = ScreenManager()
    gameClock = pygame.time.Clock()
    RUNNING = True
    while RUNNING:
        game.draw(screen)      
        pygame.display.flip()   
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == \
                  pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
            else:
                game.handleEvent(event, seconds=1)
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000       
        game.update(seconds)

    pygame.quit()

if __name__ == '__main__':
    main()