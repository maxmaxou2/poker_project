package pokermax.computer;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import pokermax.computer.utils.Combinations.Combiner;
import pokermax.computer.utils.IteratorSlicer;
import pokermax.game.Card;

public class ParallelComputer {
	
	Computer[] computers;
	int nb_process;
	public ParallelComputer() {
		this.nb_process = Runtime.getRuntime().availableProcessors();
		this.computers = new Computer[nb_process];
		for (int i = 0; i < nb_process; i++)
			this.computers[i] = new Computer();
	}
    
    public int[] estimateCountWithCards(int nb_players, int nb_try, String[] cards, int k, int nb_parts) {
        String[] rng = Card.deck(cards);
        int[] results = new int[nb_parts];
        
        //Code for end equity computing
        if (k == 0) {
        	return new int[] {this.computers[0].estimateCountWithCardsMorePlayers(nb_try, cards, nb_players), nb_try};
        }
        
        //Prepare the iterator as array
        Combiner<String> combiner = new Combiner<String>(k, rng);
        int iteratorLength = combiner.combinatorial();

        //Prepare bufferCards that we will use
        //ExecutorService executor = Executors.newCachedThreadPool();//(nb_process);
        IteratorTask[] iteratorTasks = new IteratorTask[nb_process];
        ExecutorService executor = Executors.newFixedThreadPool(nb_process);
        for (int num_process = 0; num_process < nb_process; num_process++) {
        	int[] indexes = IteratorSlicer.getSlice(num_process, iteratorLength, nb_process);
        	int length = indexes[1]-indexes[0];
        	String[][] iterations = new String[length][k];
        	for (int i = 0; i < length; i++)
            	combiner.searchNext(iterations[i]);
            iteratorTasks[num_process] = new IteratorTask(num_process, nb_process, iterations, cards, this.computers[num_process], new int[] {nb_try, nb_players, nb_parts});
            executor.submit(iteratorTasks[num_process]);
        }
        executor.shutdown();

        // Wait for all tasks to complete
        try {
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        //Perform reduction
        for (IteratorTask task : iteratorTasks) {
        	int[] resultsToSum = task.getResults();
        	for (int i = 0; i < nb_parts; i++)
        		results[i] += resultsToSum[i];
        }
        return results;
    }
    
    public double[] estimateNormalizedCountWithCards(int nb_players, int nb_try, String[] cards, int k, int nb_parts) {
        int[] results = estimateCountWithCards(nb_players, nb_try, cards, k, nb_parts);
    	
    	int max = 0;
        for (int num : results) {
            max = Math.max(max, num);
        }

        double[] normalizedResults = new double[results.length];
        for (int i = 0; i < results.length; i++) {
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

    class IteratorTask implements Runnable {
        private int[] results;
        private String[][] iterator;
        private final String[] cards;
        private int k, nb_parts, nb_players, nb_try;
        private Computer computer;

        public IteratorTask(int num_process, int nb_processes, String[][] iterator, String[] cards, Computer computer, int[] launch_params) {
            this.nb_parts = launch_params[2];
            this.nb_players = launch_params[1];
            this.nb_try = launch_params[0];
            this.iterator = iterator;
            this.cards = cards;
            this.k = iterator[0].length;
            this.computer = computer;
            this.results = new int[this.nb_parts];
        }

        @Override
        public void run() {
            String[] bufferCards = new String[cards.length+k];
            System.arraycopy(cards, 0, bufferCards, 0, cards.length);
        	for (String[] card : iterator) {
	        	System.arraycopy(card, 0, bufferCards, cards.length, k);
    			double equity = computer.estimateCountWithCardsMorePlayers(nb_try, bufferCards, nb_players) / (nb_try + 0.00001);
	            int ind = (int) (equity * nb_parts);
	            results[ind]++;
            }
        }
        
        public int[] getResults() {
        	return results;
        }
    }
}
