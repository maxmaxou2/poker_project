import json

def loadDictFromFile(filename):
    try:
        with open(filename, 'r') as file:
            loaded_dict = json.load(file)
        if loaded_dict is None :
            return {}
        else :
            return loaded_dict
    except :
        print(f"No file found, empty dictionnary provided")
        return {}

def saveDictToFile(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

def getSampleAndRemove(k, list) :
    return list[:k], list[k:]

"""
C'est Bayes en gros :
P(Gagner | Main=(card1,card2)) = P(Gagner)*P(Main=(card1,card2) | Gagner) / P(Main=(card1,card2))
= 1/nb_player * sum(storage[cartes qui t'intéressent])/nb_try * (2 parmi 52) / (2 parmi nb_cartes_qui_intéressent)
"""
def computeProbaPreFlop(nb_players, cards) :
    preflop_data_path = f"D:/Poker Project/Project/Data/pre-flop_{nb_players}.json"
    dictionnary = loadDictFromFile(preflop_data_path)

    return dictionnary[str(cards)][0]/dictionnary[str(cards)][1]

def computeProbaFlop(nb_players, cards) :
    flop_data_path = f"D:/Poker Project/Project/Data/flop_{nb_players}.json"
    dictionnary = loadDictFromFile(flop_data_path)

    return dictionnary[str(cards)][0]/dictionnary[str(cards)][1]
    
def computeProbaRiver(nb_players, cards) :
    river_data_path = f"D:/Poker Project/Project/Data/river_{nb_players}.json"
    dictionnary = loadDictFromFile(river_data_path)

    return dictionnary[str(cards)][0]/dictionnary[str(cards)][1]

if __name__ == "__main__" or True :
    pass