from Actor import RandomActor

class UserActor(RandomActor) :
    def play(self, cards, bets, current_player, banks, legal_actions) :
        ine = int(input(f"Cards : {cards}\nBets : {bets}\nCurrent : {current_player}\nBanks : {banks}\nLegal : {legal_actions}"))
        indexes = [i for i in range(len(legal_actions)) if legal_actions[i] == 1]
        while ine not in indexes :
            ine = int(input(f"Cards : {cards}\nBets : {bets}\nCurrent : {current_player}\nBanks : {banks}\nLegal : {legal_actions}"))
        return ine