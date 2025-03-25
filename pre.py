from v2.ProbaComputer import ProbaComputer
from v2.Card import Card
from itertools import combinations
import time

def loadJavaComputer() :
    jpype.startJVM(jpype.getDefaultJVMPath())

    jpype.addClassPath("D:/dependencies/pokermax-computer.jar")
    Computer = jpype.JPackage('pokermax.computer').ParallelComputer

    return Computer()

def shutdownJVM() :
    jpype.shutdownJVM()

if __name__ == "__main__" :
    import jpype

    # Start the JVM
    computer_java = loadJavaComputer()
    computer_python = ProbaComputer()

    # Call the method
    nb_players = 2
    nb_try = 20
    batch_cards = [['7h','Kd'],['8s','9h'],['Th','Ks']]#,'Ac','9d','7s']
    cards = ['As','Ah','8h','Td','Th','Ts']
    n = 2
    nb_parts = 10
    current = time.time()
    result = computer_java.estimateNormalizedCountWithCards(nb_players, 3000, cards, 1, nb_parts)
    print(time.time()-current, result)
    """current = time.time()
    result = computer_java.estimateNormalizedCountWithCards(nb_players, 700, cards, 2, nb_parts)
    print(time.time()-current, result)
    current = time.time()
    result = computer_java.estimateNormalizedCountWithCards(nb_players, 10, cards, 5, nb_parts)
    print(time.time()-current, result)"""

    shutdownJVM()

    """
    proba_computer = ProbaComputer()

    cards = ['7h','Kd','Ac','9d','7s']
    nb_try = 1000
    nb_bins = 10
    nb_players = 3
    current_time = time.time()
    results = proba_computer.estimateCountWithCardsNextNRounds(nb_players, nb_try, cards, 2, nb_bins)
    print(results)
    print(time.time()-current_time)"""

    """deck = Card.deck()
    i = 0
    for hand in combinations(deck, 2) :
        new_deck = Card.deck(hand)
        i += 1
        print(i)
        for j,table in enumerate(combinations(new_deck, 3)) :
            cards = list(hand+table)
            print(j)
            results = proba_computer.estimateCountWithCardsNextNRounds(nb_players, nb_try, cards, 2, nb_bins)"""