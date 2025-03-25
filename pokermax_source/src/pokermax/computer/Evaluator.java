package pokermax.computer;

import java.util.HashMap;

import pokermax.computer.utils.JsonRW;
import pokermax.game.Card;

public class Evaluator {

    private String ranks_table_path = "ranks.json";
    private String suits_table_path = "suits.json";
    private HashMap<Integer, Integer> ranks_map, suits_map;
    
    public Evaluator() {
        this.ranks_map = JsonRW.readJSON(this.ranks_table_path);
        this.suits_map = JsonRW.readJSON(this.suits_table_path);
    }

    public int evaluate7Cards(String[] cards) {
        int flushValue = this.retrieve7CardsFlushValue(cards);
        return flushValue > 0 ? flushValue : this.retrieve7CardsNoFlushValue(cards);
    }
    private int retrieve7CardsFlushValue(String[] cards) {
        return this.suits_map.get(Card.suit(cards[0]) + Card.suit(cards[1]) + Card.suit(cards[2]) + Card.suit(cards[3]) + Card.suit(cards[4]) + Card.suit(cards[5]) + Card.suit(cards[6]));
    }
    private int retrieve7CardsNoFlushValue(String[] cards) {
        return this.ranks_map.get(Card.rank(cards[0]) + Card.rank(cards[1]) + Card.rank(cards[2]) + Card.rank(cards[3]) + Card.rank(cards[4]) + Card.rank(cards[5]) + Card.rank(cards[6]));
    }
}
