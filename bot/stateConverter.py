import jpype
import numpy as np

def loadJavaComputer() :
    jpype.startJVM(jpype.getDefaultJVMPath())

    jpype.addClassPath("D:/dependencies/pokermax-computer.jar")
    Computer = jpype.JPackage('pokermax.computer').ParallelComputer

    return Computer()

def shutdownJVM() :
    jpype.shutdownJVM()

def processBettingHistory(betting_history) :
    features = [[-1 if bets[-1] == -1 else sum(bets) for bets in player_bets] for player_bets in betting_history]
    return features

def processPosition(nb_players, position) :
    features = [0]*nb_players
    features[position] = 1
    return [features]

def processBanks(banks) :
    return [banks]

def getState(javaComputer, cards, betting_history, position, banks) :
    distributions = computeCardsDistributions(javaComputer, len(betting_history), cards)+processPosition(len(betting_history), position)+processBanks(banks)+processBettingHistory(betting_history)
    distributions[0] = [distributions[0][0]]
    return [item for sublist in distributions for item in sublist]

nb_distributions = 3
k_steps = [[(0,200000),(3,100),(4,20),(-1,0)],[(0,200000),(0,0),(1,5000),(2,700)],[(0,200000),(0,0),(0,0),(1,3000)],[(0,200000),(0,0),(0,0),(0,0)]]
def getGroupK(cards) :
    if len(cards) == 2 :
        return k_steps[0]
    elif len(cards) == 5 :
        return k_steps[1]
    elif len(cards) == 6 :
        return k_steps[2]
    else :
        return k_steps[3]


def computeCardsDistributions(javaComputer, nb_players, cards, nb_parts=10) :
    distributions = []
    group_k = getGroupK(cards)
    for k,nb_try in group_k :
        if k == -1 :
            distributions.append(distributions[-1])
        elif nb_try == 0 :
            distributions.append([0]*nb_parts)
        else :
            distributions.append(javaComputer.estimateNormalizedCountWithCards(nb_players, nb_try, cards, k, nb_parts))
    return distributions

def computeBatchCardsDistributions(javaComputer, nb_players, batch_cards, nb_parts=10) :
    batch_distributions = []
    for cards in batch_cards :
        batch_distributions.append(computeCardsDistributions(javaComputer, nb_players, cards, nb_parts))
    return batch_distributions

if __name__ == "__main__" :
    import time
    cards = ["As", "4d","6s","3d","5d"]
    betting_history = [[[1.0, 0,0],[0],[0],[0]],[[0.5,0.5],[0],[0],[0]]]
    banks = [199, 199]
    position = 1
    java_computer = loadJavaComputer()
    current_time = time.time()
    print(getState(java_computer, cards, betting_history, position))
    print(time.time()-current_time)
    shutdownJVM()