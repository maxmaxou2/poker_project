class Card :

    ranks_map = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
    new_ranks_map = {'2':0, '3':1, '4':5, '5':22, '6':98, '7':453, '8':2031, '9':8698, 'T':22854, 'J':83661, 'Q':262349, 'K':636345, 'A':1479181}
    ranks=['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits_map = {'h':0, 'c':1, 's':2, 'd':3}
    new_suits_map = {'h':0, 'c':1, 's':8, 'd':57}
    suits=['h', 'c', 's', 'd']

    def __init__(self, rank, suit) :
        self.rank = rank
        self.suit = suit

    @staticmethod
    def oldInitFromStr(str_value) :
        return Card(Card.ranks_map[str_value[:-1]], Card.suits_map[str_value[-1]])

    @staticmethod
    def rank(str_value : str) -> int :
        return Card.new_ranks_map[str_value[0]]
    
    @staticmethod
    def suit(str_value : str) -> int :
        return Card.new_suits_map[str_value[1]]
    
    @staticmethod
    def deck(to_exclude=[]) -> list[str] :
        deck = ["" for _ in range(52-len(to_exclude))]
        index = 0
        for i,rank in enumerate(Card.ranks) :
            for j,suit in enumerate(Card.suits) :
                if rank+suit not in to_exclude :
                    deck[index] = rank+suit
                    index += 1
        return deck
    

if __name__ == "__main__" :
    deck = Card.deck()
    dic = {}
    from itertools import combinations
    from Evaluator import Evaluator

    eval = Evaluator()
    for i,combi in enumerate(combinations(deck, 7)) :
        eval.evaluate7Cards(combi)
        if i%10000 == 0:
            print("\r{:.3f}%, len: {}".format(i/134000000*100, len(dic)), end="")
    
    from jsonRW import readJSON, writeJSON
    writeJSON("./common/hashtables/suits.json", dic)