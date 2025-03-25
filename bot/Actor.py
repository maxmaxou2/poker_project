from abc import ABC, abstractmethod
import random as rd

class RandomActor(ABC):

    @abstractmethod
    def play(self, cards, bets, current_player, banks, legal_actions) :
        indexes = [i for i in range(len(legal_actions)) if legal_actions[i] == 1]
        return rd.choice(indexes)