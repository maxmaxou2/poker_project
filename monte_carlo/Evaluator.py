from common.combinations_utils import *
from common.jsonRW import readJSON
from monte_carlo.Card import Card

class Evaluator :

    ranks_map = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
    ranks=['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'] 
    suits_map = {'h':0, 'c':1, 's':2, 'd':3}
    suits=['h', 'c', 's', 'd']

    ranks_table_path = "./common/hashtables/ranks.json"
    suits_table_path = "./common/hashtables/suits.json"
    def __init__(self) :
        self.ranks_dic = readJSON(self.ranks_table_path)
        self.suits_dic = readJSON(self.suits_table_path)

        self.ranks_table = [0]*7825760
        for key in self.ranks_dic :
            self.ranks_table[int(key)] = self.ranks_dic[key]
        self.suits_table = [0]*400
        for key in self.suits_dic :
            self.suits_table[int(key)] = self.suits_dic[key]

    def evaluate7Cards(self, cards) :
        #flushValue = self.retrieve7CardsFlushValue(cards)
        return self.retrieve7CardsFlushValue(cards) if self.retrieve7CardsFlushValue(cards) > 0 else self.retrieve7CardsNoFlushValue(cards)

    def retrieve7CardsFlushValue(self, cards) :
        return self.suits_table[Card.suit(cards[0]) + Card.suit(cards[1]) + Card.suit(cards[2]) + Card.suit(cards[3]) + Card.suit(cards[4]) + Card.suit(cards[5]) + Card.suit(cards[6])]
    
    def retrieve7CardsNoFlushValue(self, cards) :
        return self.ranks_table[Card.rank(cards[0]) + Card.rank(cards[1]) + Card.rank(cards[2]) + Card.rank(cards[3]) + Card.rank(cards[4]) + Card.rank(cards[5]) + Card.rank(cards[6])]

    @staticmethod
    def compute7CardsValueFlush(cards) :
        r_counts, s_counts = countRankAndSuits(cards, Evaluator.ranks, Evaluator.suits)
        if hasFlush(r_counts, s_counts) :
            #Quinte flush ou flush tout court
            f_counts = countForFlush(cards, Evaluator.ranks, Evaluator.suits)
            quinte_flush_v = quinteFlushValue(f_counts)
            if quinte_flush_v is not None :
                #print("c")
                return (quinte_flush_v+1) << 72
            
            #print("d")
            return (flushValue(f_counts)+1) << 40 #On a dj vérifié qu'il y avait une flush donc pas besoin de reverif
        return 0
    
    rank_shifts = []
    @staticmethod
    def compute7CardsValueNoFlush(cards) :
        r_counts, s_counts = countRankAndSuits(cards, Evaluator.ranks, Evaluator.suits)
        if hasThreeOfAKindOrMore(r_counts, s_counts) :
            #Possiblement full house ou four of a kind ou three of a kind ou quinte flush ou flush
            if hasFourOfAKind(r_counts, s_counts) :
                #four of a kind, donc impossible de straight
                #print("a")
                index = fourOfAKindValue(r_counts, s_counts)
                toAdd = getRemainingHighestCardsValue(r_counts,s_counts, [index], 1)
                return ((index+1) << 68) + toAdd
            else :
                #f_house ou three of a kind ou straight
                f_house = hasFullHouse(r_counts, s_counts)
                if f_house :
                    #Full house forcément
                    #print("e")
                    return (fullHouseValue(r_counts, s_counts)+1) << 60
                else :
                    #three of a kind ou straight
                    max_length, last_index = longestSequenceAndIndex([r_counts[-1]]+r_counts)
                    if max_length >= 5 :
                        #print("f")
                        return (last_index+1) << 36 #Valeur pour straight 
                    else :
                        #three of a kind
                        #print("g")
                        index = threeOfAKindValue(r_counts, s_counts)
                        toAdd = getRemainingHighestCardsValue(r_counts,s_counts, [index], 2)
                        return ((index+1) << 32) + toAdd
        else :
            #Straight ou double paire, paire ou carte plus haute
            max_length, last_index = longestSequenceAndIndex([r_counts[-1]]+r_counts)
            if max_length >= 5 :
                #print("j")
                return (last_index+1) << 36
                    
            arr = [i for i in range(len(r_counts)) if r_counts[i] >= 2]
            if len(arr) >= 2 :
                #Double paire
                #print("k")
                indexes = doublePairValue(r_counts, s_counts)
                toAdd = getRemainingHighestCardsValue(r_counts,s_counts, indexes, 1)
                return (((indexes[0] << 4)+ indexes[1] + 1) << 24) + toAdd
            elif len(arr) == 1 :
                #Paire
                #print("l")
                toAdd = getRemainingHighestCardsValue(r_counts,s_counts, arr, 3)
                return ((arr[0]+1) << 20)+toAdd
            else :
                return getRemainingHighestCardsValue(r_counts, s_counts, [], 5)