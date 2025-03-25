import random
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from monte_carlo.Evaluator import Evaluator
from common.jsonRW import readJSON
from monte_carlo.Card import Card

def getSampleAndRemove(k, list) :
    return list[:k], list[k:]

class ProbaComputer :
    preflop_stats_path = "./hashtables/preflop_stats.json"
    def __init__(self) :
        self.turnvalues = None#Proba.loadOrSetupBlank(f"D:/Poker Project/poker_project/Data/turnvalues", 133784560)
        self.evaluator = Evaluator()
        self.preflop_stats = readJSON(self.preflop_stats_path)

    def retrievePreFlopProba(self, hand, nb_players) :
        return self.preflop_stats[hand.getCompatibleHand()][nb_players-2]
    
    def estimateCountWithCards2Players(self, nb_try, cards, nb_players) :
        rng = Card.deck(to_exclude=cards)

        player_hand, cards = getSampleAndRemove(2, cards)
        count = 0
        table_size = 5-len(cards)
        sample_size = table_size+2
        for _ in range(nb_try) :
            available = random.sample(rng, k=sample_size)

            table, available = getSampleAndRemove(table_size, available)
            table = table + cards
            hand_val = self.evaluator.evaluate7Cards(table+player_hand)

            if self.evaluator.evaluate7Cards(table+available) > hand_val :
                continue
            count += 1

        return count
    
    def estimateCountWithCardsMorePlayers(self, nb_try, cards, nb_players) :
        rng = Card.deck(to_exclude=cards)
        nb_players -= 1

        player_hand, cards = getSampleAndRemove(2, cards)
        count = 0
        table_size = 5-len(cards)
        sample_size = table_size+2*nb_players
        for _ in range(nb_try) :
            available = random.sample(rng, k=sample_size)

            table, available = getSampleAndRemove(table_size, available)
            table = table + cards
            hand_val = self.evaluator.evaluate7Cards(table+player_hand)

            hands = [0]*nb_players
            for i in range(nb_players) :
                hands[i], available = getSampleAndRemove(2, available)
            if any([self.evaluator.evaluate7Cards(table+hand) > hand_val for hand in hands]) :
                continue
            count += 1

        return count
    
    def estimateCountWithCardsNextNRounds(self, nb_players, nb_try, cards, n, nb_parts=10) :
        rng = Card.deck(to_exclude=cards)
        results = [0]*nb_parts

        if nb_players == 2 :
            to_call = self.estimateCountWithCards2Players
        else :
            to_call = self.estimateCountWithCardsMorePlayers

        if len(cards) == 2 :
            if n == 1 :
                iterator = combinations(rng, 3)
            elif n == 2 :
                iterator = combinations(rng, 4)
            elif n == 3 :
                iterator = combinations(rng, 5)
        
        elif len(cards) == 5 :
            if n == 1 :
                iterator = combinations(rng, 1)
            elif n == 2 :
                iterator = combinations(rng,2)

        elif len(cards) == 6 :
            if n == 1 :
                iterator = combinations(rng,1)

        elif len(cards) == 7 :
            equity = to_call(nb_try, cards, nb_players)/(nb_try+0.00001)
            index = int(equity*nb_parts)
            results[index] += 1
            return results
            
        for card in iterator :
            buffer_cards = cards + list(card)
            equity = to_call(nb_try, buffer_cards, nb_players)/(nb_try+0.00001)
            index = int(equity*nb_parts)
            results[index] += 1
            
        return results
    
    def scale(self, raw_outputs, a, b) :
        ma, mi = np.max(raw_outputs), np.min(raw_outputs)
        return (raw_outputs-mi)/(ma-mi)*(b-a)+a
    
    def sigmoid(self, raw_outputs):
        exp_raw_outputs = np.exp(-raw_outputs)
        probabilities = 1.0 / (1.0 + exp_raw_outputs)
        return probabilities
    
if __name__ =="__main__" :
    proba_computer = ProbaComputer()

    def run() :
        cards = ['7h','Kd','Ac','9d','7s']
        nb_try = 1000
        nb_bins = 10
        nb_players = 3
        current_time = time.time()
        results = proba_computer.estimateCountWithCardsNextNRounds(nb_players, nb_try, cards, nb_players, nb_bins)
        print(results)
        print(time.time()-current_time)
        #plt.bar([i/nb_bins for i in range(nb_bins)], results, align='edge', width=1/nb_bins)
        #plt.show()

    import cProfile, time
    #cProfile.run('run()', sort='cumulative')
    run()