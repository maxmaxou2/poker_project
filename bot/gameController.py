from UserActor import UserActor
from game import Game
from stateConverter import getState, loadJavaComputer, shutdownJVM

class GameController :
    def __init__(self, actors) :
        self.game = Game(len(actors))
        self.actors = actors
        #self.java_computer = loadJavaComputer()

    def round(self) :
        self.game.begin()
        while not self.game.isFinished() :
            current_player = self.game.nextPlayer()
            legal_actions = self.game.getCurrentLegalActions()
            banks = self.game.getBanks()
            bets = self.game.getBettingHistory()
            cards = self.game.getCards()
            choice = self.actors[current_player].play(cards, bets, current_player, banks, legal_actions) #UPDATE THIS LINE TO GET THE RIGHT OUTPUT AND COMPATIBLE WITH PYTORCH
            self.game.play(choice)
            if self.game.isRoundFinished() :
                self.game.nextStep()
        

if __name__ == "__main__" :
    game_controller = GameController([UserActor(), UserActor(), UserActor()])
    game_controller.round()