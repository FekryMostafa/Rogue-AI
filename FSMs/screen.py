from .abstract import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    game     = State()
    paused   = State()
    inStats  = State()

    pause = game.to(paused) | paused.to(game) | \
            mainMenu.to.itself(internal=True)
    stats = game.to(inStats) | inStats.to(game) | paused.to(inStats) | mainMenu.to(inStats)
    startGame = mainMenu.to(game)
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
    

    def isInGame(self):
        return self == "game" or self == "paused"
    