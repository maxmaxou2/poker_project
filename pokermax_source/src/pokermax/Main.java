package pokermax;

import java.util.Arrays;

import pokermax.computer.Computer;
import pokermax.computer.ParallelComputer;

public class Main {

	public static void main(String[] args) {
		ParallelComputer pcomputer = new ParallelComputer();
		Computer computer = new Computer();
		
		/*HashMap<Integer, Integer> hashMap = JsonRW.readJSON("ranks.json");
		for (Integer key : hashMap.keySet()) {
            int value = hashMap.get(key);
            System.out.println("Clé: " + key + ", Valeur: " + value);
        }
		
		String[] cards = new String[]{"7h","Kd","Ac","9d","7s"};
		String[] deck = Card.deck(cards);
		for (String el : deck) {
			System.out.println(el);
		}
		
		System.out.println(computer.estimateCountWithCardsMorePlayers(100000, cards, 3));*/

		String[] cards = new String[]{"9d","Ks"};//,{"8h","Kh"},{"9d","Ks"}};
		long startTime = System.currentTimeMillis();
		int k = 5;
		startTime = System.currentTimeMillis();
		System.out.println(Arrays.toString(pcomputer.estimateNormalizedCountWithCards(3, 5, cards, k, 10)));
		System.out.println((System.currentTimeMillis()-startTime)/1000.0);
		startTime = System.currentTimeMillis();
		System.out.println(Arrays.toString(computer.estimateNormalizedCountWithCards(3, 5, cards, k, 10)));
		System.out.println((System.currentTimeMillis()-startTime)/1000.0);
	}
}