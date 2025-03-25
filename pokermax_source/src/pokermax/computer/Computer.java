package pokermax.computer;

import java.util.Random;
import java.util.stream.IntStream;

import pokermax.computer.utils.Combinations.Combiner;
import pokermax.game.Card;

public class Computer {

    Evaluator evaluator;
    Random random;
    
    public Computer() {
        this.evaluator = new Evaluator();
        this.random = new Random();
    }
    
    public int estimateCountWithCards2Players(int nbTry, String[] cards, int nbPlayers) {
        String[] rng = Card.deck(cards);

        //Init playerTable and midTable
        String[] midTable = new String[7];
        String[] playerTable = new String[7];
        System.arraycopy(cards, 0, playerTable, 0, cards.length);
        System.arraycopy(cards, 2, midTable, 2, cards.length-2);
        
        int count = 0;
        for (int i = 0; i < nbTry; i++) {
        	//Shuffle and put the remaining generated table
        	shuffleArray(rng);
            System.arraycopy(rng, 0, playerTable, cards.length, 7-cards.length);
            System.arraycopy(rng, 0, midTable, cards.length, 7-cards.length);
            
            //Add the hand of opponent
            System.arraycopy(rng, 7-cards.length, midTable, 0, 2);
            
            int handVal = this.evaluator.evaluate7Cards(playerTable);

            if (this.evaluator.evaluate7Cards(midTable) > handVal)
                continue;
            count++;
        }

        return count;
    }
    
    public int estimateCountWithCardsMorePlayers(int nbTry, String[] cards, int nbPlayers) {
        String[] rng = Card.deck(cards);

        //Init playerTable and midTable
        String[] midTable = new String[7];
        String[] playerTable = new String[7];
        System.arraycopy(cards, 0, playerTable, 0, cards.length);
        System.arraycopy(cards, 2, midTable, 2, cards.length-2);
        
        int count = 0;
        nbPlayers--;
        for (int i = 0; i < nbTry; i++) {
        	//Shuffle and put the remaining generated table
        	shuffleArray(rng);
            System.arraycopy(rng, 0, playerTable, cards.length, 7-cards.length);
            System.arraycopy(rng, 0, midTable, cards.length, 7-cards.length);

            int handVal = this.evaluator.evaluate7Cards(playerTable);
            
            //Add the hand of opponent and evaluate it
            boolean found = false;
            for (int j = 0; j < nbPlayers; j++) {
            	System.arraycopy(rng, 7-cards.length+2*j, midTable, 0, 2);
            	if (this.evaluator.evaluate7Cards(midTable) > handVal) {
            		found = true;
                    break;
            	}
            }
            if (found)
            	continue;

            count++;
        }

        return count;
    }
    
    public computeFunction getFunctionToCall(int nb_players) {
    	if (nb_players == 2) {
            return this::estimateCountWithCards2Players;
        } else {
            return this::estimateCountWithCardsMorePlayers;
        }
    }
    
    public int[] getResults(int nb_try, int nb_players, String[] cards, int nb_parts) {
        int[] results = new int[nb_parts];
        double equity = this.estimateCountWithCardsMorePlayers(nb_try, cards, nb_players) / (nb_try + 0.00001);
        int index = (int) (equity * nb_parts);
        results[index]++;
        return results;
    }
    
    public int[] estimateCountWithCards(int nb_players, int nb_try, String[] cards, int k, int nb_parts) {
        String[] rng = Card.deck(cards);
        int[] results = new int[nb_parts];

        computeFunction to_call;
        if (nb_players == 2) {
            to_call = this::estimateCountWithCards2Players;
        } else {
            to_call = this::estimateCountWithCardsMorePlayers;
        }
        
        if (k == 0) {
            double equity = to_call.apply(nb_try, cards, nb_players) / (nb_try + 0.00001);
            int index = (int) (equity * nb_parts);
            results[index]++;
            return results;
        }

        // Iterate over the iterator
        String[] bufferCards = new String[cards.length+k];
        System.arraycopy(cards, 0, bufferCards, 0, cards.length);
        
        Combiner<String> combiner = new Combiner<String>(k, rng);
        String[] card = new String[k];
        while (combiner.searchNext(card)) {
        	System.arraycopy(card, 0, bufferCards, cards.length, k);
            double equity = to_call.apply(nb_try, bufferCards, nb_players) / (nb_try + 0.00001);
            int index = (int) (equity * nb_parts);
            results[index]++;
        }
        return results;
    }
    
    public double[] estimateNormalizedCountWithCards(int nb_players, int nb_try, String[] cards, int n, int nb_parts) {
    	int[] results = estimateCountWithCards(nb_players, nb_try, cards, n, nb_parts);

        int max = 0;
        for (int num : results) {
            max = Math.max(max, num);
        }

        double[] normalizedResults = new double[nb_parts];
        for (int i = 0; i < nb_parts; i++) {
        	normalizedResults[i] = (double) results[i] / max;
        }
        return normalizedResults;
    }
    
    public double[][] estimateBatchNormalizedCountWithCards(int nb_players, int nb_try, String[][] cardsBatch, int n, int nb_parts) {
    	double[][] normalizedBatchResults = new double[cardsBatch.length][cardsBatch[0].length];
    	for (int i = 0; i < cardsBatch.length; i++) {
    		String[] cards = cardsBatch[i];
    		normalizedBatchResults[i] = estimateNormalizedCountWithCards(nb_players, nb_try, cards, n, nb_parts);
    	}
    	return normalizedBatchResults;
    }
    
    interface computeFunction {
        int apply(int nb_try, String[] cards, int nb_players);
    }

    // Fisher-Yates shuffle algorithm to shuffle the array
    public <T> void shuffleArray(T[] array) {
        for (int i = array.length - 1; i > 0; i--) {
            int index = this.random.nextInt(i + 1);
            // Swap array[i] with the randomly selected element
            T temp = array[index];
            array[index] = array[i];
            array[i] = temp;
        }
    }
    
    public void shuffleArray(int[] array) {
        for (int i = array.length - 1; i > 0; i--) {
            int index = this.random.nextInt(i + 1);
            // Swap array[i] with the randomly selected element
            int temp = array[index];
            array[index] = array[i];
            array[i] = temp;
        }
	}

    // Fisher-Yates shuffle algorithm to shuffle the array
    public void randomSample(String[] array, int k) {
        int[] indexes = IntStream.range(0, array.length).toArray();
        shuffleArray(indexes);
        String[] result = new String[k];
        for (int i = 0; i < k; i++) {
            result[i] = array[indexes[i]];
        }
    }
}
