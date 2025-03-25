from Card import Card
import random as rd

class Game :
    NB_LEGAL_ACTIONS = 18
    def __init__(self, nb_players) :
        self.nb_players = nb_players
        self.table = []
        self.deck = []
        self.current_player = 0
        self.small_blind = 0
        self.playing = []
        self.played = []
        self.pot = 0
        self.step = 0

    def initBanksAndBets(self) :
        self.banks = [rd.random()*198+2 for _ in range(self.nb_players)]
        self.bets = [[[0],[0],[0],[0]] for _ in range(self.nb_players)]
        self.pot = 0

    def initPositions(self) :
        self.playing = [True]*self.nb_players
        self.played = [False]*self.nb_players
        self.is_finished = False
        self.small_blind = (self.small_blind + 1)%self.nb_players
        self.big_blind = (self.small_blind+1)%self.nb_players
        self.current_player = self.big_blind
        self.step = 0

    def deal(self) :
        self.deck = Card.deck()
        rd.shuffle(self.deck)
        k = 2*self.nb_players+5
        extract,self.deck = self.deck[:k],self.deck[k:]
        self.cards = [extract[i*2:2*i+2] for i in range(self.nb_players)]
        self.table = extract[2*self.nb_players:]

    def placeBlinds(self) :
        self.bets[self.small_blind][0][0] = min(0.5, self.banks[self.small_blind])
        self.bets[self.big_blind][0][0] = min(1, self.banks[self.big_blind])
        self.pot += 1.5

    def begin(self) :
        self.initPositions()
        self.initBanksAndBets()
        self.deal()
        self.placeBlinds()

    def getCards(self) :
        table = []
        if self.step == 1 :
            table = self.table[:3]
        elif self.step == 2 :
            table = self.table[:4]
        elif self.step == 3 :
            table = self.table[:5]
        return self.cards[self.current_player]+table

    def getCurrentLegalActions(self) :
        return self.legal_actions
    
    def getBettingHistory(self) :
        return self.bets
    
    def getBanks(self) :
        return self.banks

    def bet(self, value) :
        self.bets[self.current_player][self.step].append(value)
        self.pot += value

    def isFinished(self) :
        return sum(self.playing) < 2 or self.is_finished

    def nextPlayer(self) :
        self.current_player = (self.current_player+1)%self.nb_players
        while(not self.playing[self.current_player]) :
            self.current_player = (self.current_player+1)%self.nb_players
        self.updateCurrentLegalActions()
        return self.current_player

    def isRoundFinished(self) :
        return sum(self.played)==sum(self.playing)

    def play(self, action_number) :
        if action_number == 0 :
            self.playing[self.current_player] = False
            self.played[self.current_player] = False
        else :
            bet = 0
            if action_number == 2 :
                bet = self.to_call
            elif action_number >= 3 and action_number <= 7 :
                bet = 8-action_number
            elif action_number >= 8 and action_number <= 12 :
                bet = self.pot/(13.0-action_number)
            elif action_number >= 13 and action_number <= 18 :
                bet = self.pot/(18.0-action_number)
            self.bet(bet)

            if bet > self.to_call :
                self.played = [False]*self.nb_players
            self.played[self.current_player] = True

    def nextStep(self) :
        self.step+=1
        if self.step >= 4 :
            self.is_finished = True
            return
        self.played = [False]*self.nb_players
        self.current_player = self.big_blind

    def updateCurrentLegalActions(self) :
        actions = [1]*Game.NB_LEGAL_ACTIONS
        bank = self.banks[self.current_player]
        toCall = max([sum(self.bets[i][self.step]) for i in range(self.nb_players)])-sum(self.bets[self.current_player][self.step])
        if toCall > 0 :
            actions[1] = 0
        else :
            actions[0] = 0
            actions[2] = 0
        if bank < toCall :
            actions[2] = 0
        for i,multi in enumerate([5.0,4.0,3.0,2.0,1.0]) :
            if bank < multi or multi < toCall:
                actions[3+i] = 0
            if self.pot/multi > bank or self.pot/multi < toCall:
                actions[8+i] = 0
            if bank/multi < toCall:
                actions[13+i] = 0

        actions[17] = 1
        
        self.legal_actions = actions
        self.to_call = toCall