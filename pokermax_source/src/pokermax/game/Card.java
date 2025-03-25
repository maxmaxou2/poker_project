package pokermax.game;

import java.util.Arrays;
import java.util.HashMap;

public class Card {
	    @SuppressWarnings("serial")
		private static HashMap<Character, Integer> ranks_map = new HashMap<Character, Integer>() {{
	        put('2', 0); put('3', 1); put('4', 5); put('5', 22); put('6', 98);
	        put('7', 453); put('8', 2031); put('9', 8698); put('T', 22854); put('J', 83661);
	        put('Q', 262349); put('K', 636345); put('A', 1479181);
	    }};
	    private static String[] ranks=new String[]{"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};

	    @SuppressWarnings("serial")
		private static HashMap<Character, Integer> suits_map = new HashMap<Character, Integer>() {{
	        put('h', 0); put('c', 1); put('s', 8); put('d', 57);
	    }};
	    private static String[] suits = new String[]{"h", "c", "s", "d"};

	    public int rank, suit;
	    public Card(int rank, int suit) {
	        this.rank = rank;
	        this.suit = suit;
	    }

		public static Card initFromStr(String str_value) {
	        return new Card(Card.ranks_map.get(str_value.charAt(0)), Card.suits_map.get(str_value.charAt(1)));
	    }

		public static int rank(String str_value ) {
	        return Card.ranks_map.get(str_value.charAt(0));
	    }

		public static int suit(String str_value ) {
	        return Card.suits_map.get(str_value.charAt(1));
	    }
	    
	    public static String[] deck(String[] to_exclude) {
	        String[] deck = new String[52-to_exclude.length];
	        int index = 0;
	        for (int i = 0; i < ranks.length; i++) {
	            for (int j = 0; j < suits.length; j++) {
	                String card = ranks[i] + suits[j];
	                if (!Arrays.stream(to_exclude).anyMatch(card::equals)) {
	                    deck[index] = card;
	                    index++;
	                }
	            }
	        }
	        return deck;
	    }
}
