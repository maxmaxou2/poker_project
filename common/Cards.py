from itertools import combinations
import random as rd
import time
from common.utils import *
from common.combinations_utils import *

preflop_stats = {
    "A-A":[85.3,73.4,63.9,55.9,49.2,43.6,38.8,34.7,31.1],
    "A-Ks":[67.0,50.7,41.4,35.4,31.1,27.7,25.0,22.7,20.7],
    "A-K":[65.4,48.2,38.6,32.4,27.9,24.4,21.6,19.2,17.2],
    "A-Qs":[66.1,49.4,39.9,33.7,29.4,26.0,23.3,21.1,19.3],
    "A-Q":[64.5,46.8,36.9,30.4,25.9,22.5,19.7,17.5,15.5],
    "A-Js":[65.4,48.2,38.5,32.2,27.8,24.5,22.0,19.9,18.1],
    "A-J":[63.6,45.6,35.4,28.9,24.4,21.0,18.3,16.1,14.3],
    "A-10s":[64.7,47.1,37.2,31.0,26.7,23.5,21.0,18.9,17.3],
    "A-10":[62.9,44.4,34.1,27.6,23.1,19.8,17.2,15.1,13.4],
    "A-9s":[63.0,44.8,34.6,28.4,24.2,21.1,18.8,16.9,15.4],
    "A-9":[60.9,41.8,31.2,24.7,20.3,17.1,14.7,12.8,11.2],
    "A-8s":[62.1,43.7,33.6,27.4,23.3,20.3,18.0,16.2,14.8],
    "A-8":[60.1,40.8,30.1,23.7,19.4,16.2,13.9,12.0,10.6],
    "A-7s":[61.1,42.6,32.6,26.5,22.5,19.6,17.4,15.7,14.3],
    "A-7":[59.1,39.4,28.9,22.6,18.4,15.4,13.2,11.4,10.1],
    "A-6s":[60.0,41.3,31.4,25.6,21.7,19.0,16.9,15.3,14.0],
    "A-6":[57.8,38.0,27.6,21.5,17.5,14.7,12.6,10.9,9.6],
    "A-5s":[59.9,41.4,31.8,26.0,22.2,19.6,17.5,15.9,14.5],
    "A-5":[57.7,38.2,27.9,22.0,18.0,15.2,13.1,11.5,10.1],
    "A-4s":[58.9,40.4,30.9,25.3,21.6,19.0,17.0,15.5,14.2],
    "A-4":[56.4,36.9,26.9,21.1,17.3,14.7,12.6,11.0,9.8],
    "A-3s":[58.0,39.4,30.0,24.6,21.0,18.5,16.6,15.1,13.9],
    "A-3":[55.6,35.9,26.1,20.4,16.7,14.2,12.2,10.7,9.5],
    "A-2s":[57.0,38.5,29.2,23.9,20.4,18.0,16.1,14.6,13.4],
    "A-2":[54.6,35.0,25.2,19.6,16.1,13.6,11.7,10.2,9.1],
    "K-K":[82.4,68.9,58.2,49.8,43.0,37.5,32.9,29.2,26.1],
    "K-Qs":[63.4,47.1,38.2,32.5,28.3,25.1,22.5,20.4,18.6],
    "K-Q":[61.4,44.4,35.2,29.3,25.1,21.8,19.1,16.9,15.1],
    "K-Js":[62.6,45.9,36.8,31.1,26.9,23.8,21.3,19.3,17.6],
    "K-J":[60.6,43.1,33.6,27.6,23.5,20.2,17.7,15.6,13.9],
    "K-10s":[61.9,44.9,35.7,29.9,25.8,22.8,20.4,18.5,16.9],
    "K-10":[59.9,42.0,32.5,26.5,22.3,19.2,16.7,14.7,13.1],
    "K-9s":[60.0,42.4,32.9,27.2,23.2,20.3,18.1,16.3,14.8],
    "K-9":[58.0,39.5,29.6,23.6,19.5,16.5,14.1,12.3,10.8],
    "K-8s":[58.5,40.2,30.8,25.1,21.3,18.6,16.5,14.8,13.5],
    "K-8":[56.3,37.2,27.3,21.4,17.4,14.6,12.5,10.8,9.4],
    "K-7s":[57.8,39.4,30.1,24.5,20.8,18.1,16.0,14.5,13.2],
    "K-7":[55.4,36.1,26.3,20.5,16.7,13.9,11.8,10.2,9.0],
    "K-6s":[56.8,38.4,29.1,23.7,20.1,17.5,15.6,14.0,12.8],
    "K-6":[54.3,35.0,25.3,19.7,16.0,13.3,11.3,9.8,8.6],
    "K-5s":[55.8,37.4,28.2,23.0,19.5,17.0,15.2,13.7,12.5],
    "K-5":[53.3,34.0,24.5,19.0,15.4,12.9,11.0,9.5,8.3],
    "K-4s":[54.7,36.4,27.4,22.3,19.0,16.6,14.8,13.4,12.3],
    "K-4":[52.1,32.8,23.4,18.1,14.7,12.3,10.5,9.1,8.0],
    "K-3s":[53.8,35.5,26.7,21.7,18.4,16.2,14.5,13.1,12.1],
    "K-3":[51.2,31.9,22.7,17.6,14.2,11.9,10.2,8.9,7.8],
    "K-2s":[52.9,34.6,26.0,21.2,18.1,15.9,14.3,13.0,11.9],
    "K-2":[50.2,30.9,21.8,16.9,13.7,11.5,9.8,8.6,7.6],
    "Q-Q":[79.9,64.9,53.5,44.7,37.9,32.5,28.3,24.9,22.2],
    "Q-Js":[60.3,44.1,35.6,30.1,26.1,23.0,20.7,18.7,17.1],
    "Q-J":[58.2,41.4,32.6,26.9,22.9,19.8,17.3,15.3,13.7],
    "Q-10s":[59.5,43.1,34.6,29.1,25.2,22.3,19.9,18.1,16.6],
    "Q-10":[57.4,40.2,31.3,25.7,21.6,18.6,16.3,14.4,12.9],
    "Q-9s":[57.9,40.7,31.9,26.4,22.5,19.7,17.6,15.9,14.5],
    "Q-9":[55.5,37.6,28.5,22.9,19.0,16.1,13.8,12.1,10.7],
    "Q-8s":[56.2,38.6,29.7,24.4,20.7,18.0,16.0,14.4,13.2],
    "Q-8":[53.8,35.4,26.2,20.6,16.9,14.1,12.1,10.5,9.2],
    "Q-7s":[54.5,36.7,27.9,22.7,19.2,16.7,14.8,13.3,12.1],
    "Q-7":[51.9,33.2,24.0,18.6,15.1,12.5,10.6,9.2,8.0],
    "Q-6s":[53.8,35.8,27.1,21.9,18.5,16.1,14.3,12.9,11.7],
    "Q-6":[51.1,32.3,23.2,17.9,14.4,12.0,10.1,8.8,7.6],
    "Q-5s":[52.9,34.9,26.3,21.4,18.1,15.8,14.1,12.7,11.6],
    "Q-5":[50.2,31.3,22.3,17.3,13.9,11.6,9.8,8.5,7.4],
    "Q-4s":[51.7,33.9,25.5,20.7,17.6,15.4,13.7,12.4,11.3],
    "Q-4":[49.0,30.2,21.4,16.4,13.3,11.0,9.4,8.1,7.1],
    "Q-3s":[50.7,33.0,24.7,20.1,17.0,14.9,13.3,12.1,11.1],
    "Q-3":[47.9,29.2,20.7,15.9,12.8,10.7,9.1,7.9,6.9],
    "Q-2s":[49.9,32.2,24.0,19.5,16.6,14.6,13.1,11.9,10.9],
    "Q-2":[47.0,28.4,19.9,15.3,12.3,10.3,8.8,7.7,6.8],
    "J-J":[77.5,61.2,49.2,40.3,33.6,28.5,24.6,21.6,19.3],
    "J-10s":[57.5,41.9,33.8,28.5,24.7,21.9,19.7,17.9,16.5],
    "J-10":[55.4,39.0,30.7,25.3,21.5,18.6,16.3,14.5,13.1],
    "J-9s":[55.8,39.6,31.3,26.1,22.4,19.7,17.6,15.9,14.6],
    "J-9":[53.4,36.5,27.9,22.5,18.7,15.9,13.8,12.1,10.8],
    "J-8s":[54.2,37.5,29.1,24.0,20.5,17.9,15.9,14.4,13.2],
    "J-8":[51.7,34.2,25.6,20.4,16.8,14.1,12.2,10.7,9.5],
    "J-7s":[52.4,35.4,27.1,22.2,18.9,16.4,14.6,13.2,12.0],
    "J-7":[49.9,32.1,23.5,18.3,14.9,12.4,10.6,9.2,8.1],
    "J-6s":[50.8,33.6,25.4,20.6,17.4,15.2,13.5,12.1,11.1],
    "J-6":[47.9,29.8,21.4,16.5,13.2,11.0,9.3,8.0,7.0],
    "J-5s":[50.0,32.8,24.7,20.0,17.0,14.7,13.1,11.8,10.8],
    "J-5":[47.1,29.1,20.7,15.9,12.8,10.6,8.9,7.7,6.7],
    "J-4s":[49.0,31.8,24.0,19.4,16.4,14.3,12.8,11.5,10.6],
    "J-4":[46.1,28.1,19.9,15.3,12.3,10.2,8.6,7.5,6.5],
    "J-3s":[47.9,30.9,23.2,18.8,16.0,14.0,12.5,11.3,10.4],
    "J-3":[45.0,27.1,19.1,14.6,11.7,9.8,8.3,7.2,6.3],
    "J-2s":[47.1,30.1,22.6,18.3,15.6,13.7,12.2,11.1,10.2],
    "J-2":[44.0,26.2,18.4,14.1,11.3,9.4,8.0,7.0,6.2],
    "10-10":[75.1,57.7,45.2,36.4,30.0,25.3,21.8,19.2,17.2],
    "10-9s":[54.3,38.9,31.0,26.0,22.5,19.8,17.8,16.2,14.9],
    "10-9":[51.7,35.7,27.7,22.5,18.9,16.2,14.1,12.6,11.3],
    "10-8s":[52.6,36.9,29.0,24.0,20.6,18.1,16.2,14.8,13.6],
    "10-8":[50.0,33.6,25.4,20.4,16.9,14.4,12.5,11.0,9.9],
    "10-7s":[51.0,34.9,27.0,22.2,19.0,16.6,14.8,13.5,12.4],
    "10-7":[48.2,31.4,23.4,18.4,15.1,12.8,11.0,9.7,8.6],
    "10-6s":[49.2,32.8,25.1,20.5,17.4,15.2,13.6,12.3,11.2],
    "10-6":[46.3,29.2,21.2,16.5,13.4,11.2,9.5,8.3,7.3],
    "10-5s":[47.2,30.8,23.3,18.9,16.0,13.9,12.4,11.2,10.2],
    "10-5":[44.2,27.1,19.3,14.8,11.9,9.9,8.4,7.2,6.4],
    "10-4s":[46.4,30.1,22.7,18.4,15.6,13.6,12.1,11.0,10.0],
    "10-4":[43.4,26.4,18.7,14.3,11.5,9.5,8.1,7.0,6.2],
    "10-3s":[45.5,29.3,22.0,17.8,15.1,13.2,11.8,10.7,9.8],
    "10-3":[42.4,25.5,18.0,13.7,11.0,9.1,7.8,6.8,6.0],
    "10-2s":[44.7,28.5,21.4,17.4,14.8,13.0,11.6,10.5,9.7],
    "10-2":[41.5,24.7,17.3,13.2,10.6,8.8,7.5,6.6,5.8],
    "9-9":[72.1,53.5,41.1,32.6,26.6,22.4,19.4,17.2,15.6],
    "9-8s":[51.1,36.0,28.5,23.6,20.2,17.8,15.9,14.5,13.4],
    "9-8":[48.4,32.9,25.1,20.1,16.6,14.2,12.3,10.9,9.9],
    "9-7s":[49.5,34.2,26.8,22.1,18.9,16.6,14.9,13.6,12.5],
    "9-7":[46.7,30.9,23.1,18.4,15.1,12.8,11.1,9.8,8.8],
    "9-6s":[47.7,32.3,24.9,20.4,17.4,15.3,13.7,12.4,11.4],
    "9-6":[44.9,28.8,21.2,16.6,13.5,11.4,9.8,8.7,7.8],
    "9-5s":[45.9,30.4,23.2,18.8,16.0,13.9,12.4,11.3,10.3],
    "9-5":[42.9,26.7,19.2,14.8,12.0,10.0,8.5,7.4,6.6],
    "9-4s":[43.8,28.4,21.3,17.3,14.6,12.7,11.3,10.3,9.4],
    "9-4":[40.7,24.6,17.3,13.2,10.5,8.7,7.3,6.4,5.6],
    "9-3s":[43.2,27.8,20.8,16.8,14.3,12.5,11.1,10.1,9.2],
    "9-3":[39.9,23.9,16.7,12.7,10.1,8.3,7.1,6.1,5.4],
    "9-2s":[42.3,27.0,20.2,16.4,13.9,12.2,10.9,9.9,9.1],
    "9-2":[38.9,22.9,16.0,12.1,9.6,8.0,6.8,5.9,5.2],
    "8-8":[69.1,49.9,37.5,29.4,24.0,20.3,17.7,15.8,14.4],
    "8-7s":[48.2,33.9,26.6,22.0,18.9,16.7,15.0,13.7,12.7],
    "8-7":[45.5,30.6,23.2,18.5,15.4,13.1,11.5,10.3,9.3],
    "8-6s":[46.5,32.0,25.0,20.6,17.6,15.6,14.1,12.9,11.9],
    "8-6":[43.6,28.6,21.3,16.9,13.9,11.8,10.4,9.2,8.3],
    "8-5s":[44.8,30.2,23.2,19.1,16.3,14.3,12.9,11.8,10.9],
    "8-5":[41.7,26.5,19.4,15.2,12.4,10.5,9.1,8.1,7.3],
    "8-4s":[42.7,28.1,21.4,17.4,14.8,13.0,11.7,10.6,9.8],
    "8-4":[39.6,24.4,17.5,13.4,10.8,9.0,7.8,6.8,6.1],
    "8-3s":[40.8,26.3,19.8,16.0,13.6,11.9,10.7,9.7,8.9],
    "8-3":[37.5,22.4,15.7,11.9,9.5,7.9,6.7,5.8,5.1],
    "8-2s":[40.3,25.8,19.4,15.7,13.3,11.7,10.5,9.6,8.8],
    "8-2":[36.8,21.7,15.1,11.4,9.1,7.5,6.4,5.6,4.9],
    "7-7":[66.2,46.4,34.4,26.8,21.9,18.6,16.4,14.8,13.7],
    "7-6s":[45.7,32.0,25.1,20.8,18.0,15.9,14.4,13.2,12.3],
    "7-6":[42.7,28.5,21.5,17.1,14.2,12.2,10.8,9.6,8.8],
    "7-5s":[43.8,30.1,23.4,19.4,16.7,14.8,13.4,12.3,11.4],
    "7-5":[40.8,26.5,19.7,15.5,12.8,11.0,9.7,8.7,7.9],
    "7-4s":[41.8,28.2,21.7,17.9,15.3,13.5,12.2,11.2,10.4],
    "7-4":[38.6,24.5,17.9,13.9,11.4,9.7,8.5,7.6,6.8],
    "7-3s":[40.0,26.3,20.0,16.4,14.0,12.3,11.1,10.1,9.3],
    "7-3":[36.6,22.4,16.0,12.3,9.9,8.4,7.2,6.4,5.7],
    "7-2s":[38.1,24.5,18.4,15.0,12.8,11.2,10.1,9.2,8.5],
    "7-2":[34.6,20.4,14.2,10.7,8.6,7.2,6.1,5.4,4.8],
    "6-6":[63.3,43.2,31.5,24.5,20.1,17.3,15.4,14.0,13.1],
    "6-5s":[43.2,30.2,23.7,19.7,17.0,15.2,13.8,12.7,11.9],
    "6-5":[40.1,26.7,20.0,15.9,13.3,11.5,10.2,9.2,8.5],
    "6-4s":[41.4,28.5,22.1,18.4,15.9,14.2,12.9,11.9,11.1],
    "6-4":[38.0,24.7,18.2,14.4,12.0,10.3,9.2,8.3,7.6],
    "6-3s":[39.4,26.5,20.4,16.8,14.5,12.9,11.7,10.8,10.0],
    "6-3":[35.9,22.7,16.4,12.8,10.6,9.1,8.0,7.2,6.5],
    "6-2s":[37.5,24.8,18.8,15.4,13.3,11.8,10.7,9.8,9.1],
    "6-2":[34.0,20.7,14.6,11.2,9.1,7.8,6.8,6.0,5.4],
    "5-5":[60.3,40.1,28.8,22.4,18.5,16.0,14.4,13.2,12.3],
    "5-4s":[41.1,28.8,22.6,18.9,16.5,14.8,13.5,12.5,11.7],
    "5-4":[37.9,25.2,18.8,15.0,12.6,11.0,9.8,8.9,8.2],
    "5-3s":[39.3,27.1,21.1,17.5,15.2,13.7,12.5,11.6,10.8],
    "5-3":[35.8,23.3,17.1,13.6,11.4,9.9,8.8,8.0,7.3],
    "5-2s":[37.5,25.3,19.5,16.1,14.0,12.5,11.4,10.6,9.8],
    "5-2":[33.9,21.3,15.3,12.0,10.0,8.6,7.6,6.8,6.2],
    "4-4":[57.0,36.8,26.3,20.6,17.3,15.2,13.9,12.9,12.1],
    "4-3s":[38.0,26.2,20.3,16.9,14.7,13.1,12.0,11.1,10.3],
    "4-3":[34.4,22.3,16.3,12.8,10.7,9.3,8.3,7.5,6.8],
    "4-2s":[36.3,24.6,18.8,15.7,13.7,12.3,11.2,10.4,9.6],
    "4-2":[32.5,20.5,14.7,11.5,9.5,8.3,7.3,6.6,6.0],
    "3-3":[53.7,33.5,23.9,19.0,16.2,14.6,13.5,12.6,12.0],
    "3-2s":[35.1,23.6,18.0,14.9,13.0,11.7,10.7,9.9,9.2],
    "3-2":[31.2,19.5,13.9,10.8,8.9,7.7,6.8,6.1,5.6],
    "2-2":[50.3,30.7,22.0,17.8,15.5,14.2,13.3,12.5,12.0]
    }

class Hand : 
    def __init__(self, hand):
        self._cards = hand
        self.sortByRank()

    def __add__(self, other) :
        return self._cards + other._cards

    def __setitem__(self, item, value):
        self._cards[item]=value

    def __getitem__(self, item):
        return self._cards[item]
    
    def __str__(self) :
        """if self._cards[0].suit == self._cards[1].suit :
            return str(self._cards[0])+"-"+str(self._cards[1])+'s'"""
        return str(self._cards[0])+"-"+str(self._cards[1])

    def sortByRank(self) :
        if self._cards[0].rank > self._cards[1].rank :
            self._cards = [self._cards[1], self._cards[0]]
        elif self._cards[1].rank == self._cards[0].rank and self._cards[0].suit > self._cards[1].suit :
            self._cards = [self._cards[1], self._cards[0]]

    """
        Input : ("9-7")
        Output : ["9h-7s", ...]
    """

    def generateAllKeysFromRanks(hand : str, suited = None) :
        arr = hand.split("-")
        rank1, rank2 = arr[0], arr[1]
        if Card.getIndexFromRank(rank1) < Card.getIndexFromRank(rank2) :
            rank1,rank2 = rank2,rank1

        keys = []
        if suited is None :
            if rank1==rank2 :
                for j in range(len(Card.suits)) :
                    for i in range(j+1, len(Card.suits)) :
                        keys.append(rank1+Card.suits[i]+"-"+rank2+Card.suits[j])
            else :
                for j in range(len(Card.suits)) :
                    for i in range(len(Card.suits)) :
                        keys.append(rank1+Card.suits[i]+"-"+rank2+Card.suits[j])
        elif suited :
            if rank1==rank2 :
                for suit1, suit2 in [("d","h"),("s", "c")] :
                    keys.append(rank1+suit1+"-"+rank2+suit2)
            else :
                for suit1, suit2 in [("d","h"),("s", "c"),("d","d"),("c", "c"),("h","h"),("s", "s")] :
                    keys.append(rank1+suit1+"-"+rank2+suit2)
            suits=['h', 'c', 's', 'd']
        else :
            if rank1==rank2 :
                for suit1, suit2 in [("s","h"),("c","h"),("d","c"),("d","s")] :
                    keys.append(rank1+suit1+"-"+rank2+suit2)
            else :
                for suit1, suit2 in [("h","s"),("h","c"),("c","d"),("s","d"),("h","h"),("c","c"),("d","d"),("s","s")] :
                    keys.append(rank1+suit2+"-"+rank2+suit1)
        return keys
    
    def strArr(self) :
        return [str(self._cards[0]), str(self._cards[1])]
    
    def isSuited(self) : 
        if self._cards[0].suit == self._cards[1].suit : 
            return True 
        else :
            return False 
    
    def getCompatibleHand(self) : 
        if self.isSuited() : 
            return(str(Card.ranks[self._cards[1].rank])+'-'+str(Card.ranks[self._cards[0].rank])+'s')
        else : 
            return(str(Card.ranks[self._cards[1].rank])+'-'+str(Card.ranks[self._cards[0].rank]))
    
class Table :

    def __init__(self, cards) :
        self._cards = cards
        self.sortByRank()

    def initFromKey(cards_str) :
        arr = cards_str.strip().split("-")
        return Table([Card.initFromStr(c_str) for c_str in arr])

    def __add__(self, other) :
        return self._cards + other._cards

    def __setitem__(self, item, value):
        self._cards[item]=value

    def __len__(self) :
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]
    
    def __str__(self) :
        ans = str(self._cards[0])
        for i in range(1, len(self._cards)) :
            ans += "-" + str(self._cards[i])
        return ans
    
    def setupStr(self) :
        self.string = [str(card) for card in self._cards]
    
    def sortByRank(self) :
        self._cards = sorted(self._cards, key=lambda card: (card.rank, card.suit))

    def explicitValue(value) :
        for i in range(len(Table.shifts)) :
            v_shifted = value >> Table.shifts[i]
            if v_shifted > 0 :
                return f"{value} : {Table.display[i]}"
            
    def explicitKey(value) :
        for i in range(len(Table.shifts)) :
            v_shifted = value >> Table.shifts[i]
            if v_shifted > 0 :
                return f"{Table.displayKey[i]}"
            
    displayKey = ["QuinteF", "4ofAK",
               "FullH", "Flush",
               "Straight", "3ofAK",
               "2 Pairs", "Pair",
               "HighC"]

    display = ["Quinte Flush", "Four Of A Kind",
               "Full House", "Flush", "Straight",
               "Three Of A Kind", "Double Pair",
               "Pair", "High Card"]
    
    shifts = [72, 68, 60, 40, 36, 32, 24, 20, 0]

    """
        
    Value de rank pour la plupart a besoin de 13 valeurs différent : 4 bits
    Value de rank pour getFullHouseValue a besoin de 8 bits (13 * 12)
    Valeur de getFlushValue a besoin de 13*12*11*10*9 -> 20 bits
    Valeur de getDoublePairValue a besoin de 8 bits

    Dans l'ordre :
    - 4 bits QuinteFlush : 72
    - 4 bits FourOfAKind : 68
    - 8 bits FullHouse : 60
    - 20 bits Flush : 40
    - 4 bits Straight : 36
    - 4 bits ThreeOfAKind : 32
    - 8 bits DoublePair : 28
    - 4 bits Pair : 20
    - 16 bits HighCard : 16

    -> 76 bits

    """

    def new_getHighestValue(self, hand :Hand = None) :
        if hand is None :
            cards = self
        else :
            cards = self + hand
        r_counts, s_counts = countRankAndSuits(cards, Card.ranks, Card.suits)
        if hasThreeOfAKindOrMore(r_counts, s_counts) :
            #Possiblement full house ou four of a kind ou three of a kind ou quinte flush ou flush
            if hasFourOfAKind(r_counts, s_counts) :
                #four of a kind, donc impossible de straight
                #print("a")
                index = fourOfAKindValue(r_counts, s_counts)
                toAdd = getRemainingHighestCardsValue(r_counts,s_counts, [index], 1)
                return ((index+1) << 68) + toAdd
            elif hasFlush(r_counts, s_counts) :
                #quinte flush ou f_house ou flush tt court
                if hasFullHouse(r_counts, s_counts) :
                    #Full house forcément
                    #print("b")
                    return (fullHouseValue(r_counts, s_counts)+1) << 60
                else :
                    #Quinte flush ou flush tout court
                    f_counts = countForFlush(cards, Card.ranks, Card.suits)
                    quinte_flush_v = quinteFlushValue(f_counts)
                    if quinte_flush_v is not None :
                        #print("c")
                        return (quinte_flush_v+1) << 72
                    
                    #print("d")
                    return (flushValue(f_counts)+1) << 40 #On a dj vérifié qu'il y avait une flush donc pas besoin de reverif
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
            if hasFlush(r_counts, s_counts) :
                #Quinte flush ou flush tout court
                f_counts = countForFlush(cards, Card.ranks, Card.suits)
                quinte_flush_v = quinteFlushValue(f_counts)
                if quinte_flush_v is not None :
                    #print("h")
                    return (quinte_flush_v+1) << 72
                
                #print("i")
                return (flushValue(f_counts)+1) << 40
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
                        
    def v3_getHighestValue(self, hand: Hand, store) :
        return store.readValuesOneD(store.getIdCards(self._cards + hand._cards))[0]
        
class Card :

    ranks_map = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
    ranks=['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'] 
    suits_map = {'h':0, 'c':1, 's':2, 'd':3}
    suits=['h', 'c', 's', 'd']

    def initFromStr(rank_and_suit) :
        rank, suit = rank_and_suit[:-1], rank_and_suit[-1]
        return Card(Card.ranks_map[rank],Card.suits_map[suit])

    def __init__(self, rank, suit) :
        self.rank = rank
        self.suit = suit
        self.code = (self.rank << 4) + self.suit

    def __str__ (self) :
        return self.ranks[self.rank]+self.suits[self.suit]

    def getRank(self) : 
        return self.rank
    
    def getIndexFromRank(rank : str) :
        return Card.ranks.index(rank)
    
if __name__ == "__main__" :
    from utils import saveDictToFile, loadDictFromFile
    import random
    
    nb_players = 4
    nb_try = 20 * 1000000

    deck = [Card(i%13,i//13) for i in range(52)]

    cards = Table.initFromKey("2c-3h-4d-5d-8c-6c-Ks")
    r_counts, s_counts = countRankAndSuits(cards, Card.ranks, Card.suits)
    print(longestSequenceAndIndex([r_counts[-1]]+r_counts))

    """r_counts, s_counts = countRankAndSuits(cards, Card.ranks, Card.suits)
    print(hasFourOfAKind(r_counts, s_counts))"""

    """store_path = f"D:/Poker Project/Project/Data/store_keyint2_{nb_players}.json"
    store = loadDictFromFile(store_path)
    i = 1
    for hand in combinations(deck, 2) :
        if i%1 == 0:
            print(f"{i/1326*100}%                 ", end="\r")
        
        for sub in combinations(deck, 3) :
            if hand[0] not in sub and hand[1] not in sub :
                arr = sorted([c.code for c in hand]+[card.code for card in sub])
                #print(arr)
                key1 = (arr[0] << 6) + arr[1]
                key2 = (arr[2] << 12) + (arr[3] << 6) + arr[4]
                table = Table(sub)
                if key1 not in store :
                    store[key1] = {}
                store[key1][key2] = Table.highestValue(table._cards)
                #print(len(store))
        i+=1
    saveDictToFile(store, store_path)

    current_time = time.time()
    preflop_data_path = f"D:/Poker Project/Project/Data/pre-flop_{nb_players}.json"
    storage_preflop = loadDictFromFile(preflop_data_path)
    for sub in combinations(deck, 2) :
        name = str(Hand(sub))
        if not name in storage_preflop :
            storage_preflop[name] = [0,0]
        else :
            break
    print(f"Loaded pre-flop in {time.time()-current_time}s")

    current_time = time.time()
    flop_data_path = f"D:/Poker Project/Project/Data/flop_{nb_players}.json"
    storage_flop = loadDictFromFile(flop_data_path)
    for sub in combinations(deck, 5) :
        name = str(Table(sub))
        if not name in storage_flop :
            storage_flop[name] = [0,0]
        else :
            break
    print(f"Loaded flop in {time.time()-current_time}s")
    
    current_time = time.time()
    river_data_path = f"D:/Poker Project/Project/Data/river_{nb_players}.json"
    storage_river = loadDictFromFile(river_data_path)
    for sub in combinations(deck, 6) :
        name = str(Table(sub))
        if not name in storage_river :
            storage_river[name] = [0,0]
        else :
            break
    print(f"Loaded river in {time.time()-current_time}s")"""

    """
    def old_getSampleAndRemove(k, list) :
        ans = []
        for _ in range(k) :
            card_index = rd.randint(0, len(list)-1)
            ans.append(list[card_index])
            del list[card_index]
        return ans"""
    
    def getSampleAndRemove(k, list) :
        return list[:k], list[k:]

    #orig_hand = Hand([Card(0, 0), Card(1,1)])
    #print(str(orig_hand[0]), str(orig_hand[1]))
    
    arr = range(0, 52)
    def run() :
        current_time = time.time()
        for n in range(nb_try) :
            random_array = random.sample(arr, k=5+2*nb_players)
            #hands = [orig_hand]
            hands = []
            if n % 10000 == 0 :
                print(f"{int(n/nb_try*100*100)/100}%, {time.time()-current_time}", end="\r")
            #available = [Card(i%13,i//13) for i in range(13*4) if all(i%13 != hands[0][j].rank or i%4 != hands[0][j].suit for j in [0,1])]
            available = [Card(i%13,i//13) for i in random_array]

            for i in range(nb_players) :
                sample, available = getSampleAndRemove(2, available)
                hands.append(Hand(sample))

            sample, available = getSampleAndRemove(5, available)
            table = Table(sample)
            table.setupStr()
            #values = [table.getHighestValue(hand) for hand in hands]
            #explicit = [Table.explicitValue(value) for value in values]
            #values = [table.v3_getHighestValue(hand, store) for hand in hands]
            values = [table.new_getHighestValue(hand) for hand in hands]
            
            explicit = [Table.explicitValue(value) for value in values]

            print(explicit)
            print(f"Table : {table}, hands : {','.join(str(hand) for hand in hands)}")
            #print(sum([abs(values[i]-new_values[i]) for i in range(len(values))]))

            max_indexes, max_value = [0], values[0]
            for i in range(1, len(values)) :
                if values[i] > max_value :
                    max_indexes, max_value = [i], values[i]
                elif values[i] == max_value :
                    max_indexes += [i]

            """for ind in max_indexes :
                storage_river[str(Table(hands[ind]._cards+table._cards[:4]))][0] += int(1000/len(max_indexes))/1000
                storage_flop[str(Table(hands[ind]._cards+table._cards[:3]))][0] += int(1000/len(max_indexes))/1000
                storage_preflop[str(hands[ind])][0] += int(1000/len(max_indexes))/1000

            for hand in hands :
                storage_river[str(Table(hand._cards+table._cards[:4]))][1] += 1
                storage_flop[str(Table(hand._cards+table._cards[:3]))][1] += 1
                storage_preflop[str(hand)][1] += 1
            """
        print(f"Elapsed Time : {int((time.time() - current_time)*100)/100}s")

        """if not "nb_try" in storage_preflop :
            storage_preflop['nb_try'] = 0
        storage_preflop["nb_try"] += nb_try
        storage_preflop["nb_players"] = nb_players

        if not "nb_try" in storage_flop :
            storage_flop['nb_try'] = 0
        storage_flop["nb_try"] += nb_try
        storage_flop["nb_players"] = nb_players

        if not "nb_try" in storage_river :
            storage_river['nb_try'] = 0
        storage_river["nb_try"] += nb_try
        storage_river["nb_players"] = nb_players
        #print(storage)
        current_time = time.time()
        saveDictToFile(storage_preflop, preflop_data_path)
        print(f"Saved pre-flop in {time.time()-current_time}s")
        current_time = time.time()
        saveDictToFile(storage_flop, flop_data_path)
        print(f"Saved flop in {time.time()-current_time}s")
        current_time = time.time()
        saveDictToFile(storage_river, river_data_path)
        print(f"Saved river in {time.time()-current_time}s")"""
        

    import cProfile
    cProfile.run('run()', sort='cumulative')
    run()
    
    """user_input = ""
    while True :
        nb_players = input("Enter nb_players : ")
        if nb_players in ["e", "ex", "exi", "exit", "quit", "stop"] :
            break
        user_input = input("Enter cards : ")
        if user_input in ["e", "ex", "exi", "exit", "quit", "stop"] :
            break
        try :
            cards = Table.initFromStr(user_input)
            if len(cards) == 2 :
                print(computeProbaPreFlop(int(nb_players), cards))
            elif len(cards) == 5 :
                print(computeProbaFlop(int(nb_players), cards))
            elif len(cards) == 6 :
                print(computeProbaRiver(int(nb_players), cards))
        except :
            print("Error ! If you want to exit, type exit")"""