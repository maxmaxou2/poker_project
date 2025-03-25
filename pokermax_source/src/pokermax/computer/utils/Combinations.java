package pokermax.computer.utils;

import java.util.Arrays;

public class Combinations {
	public static void main( String[] args )
	{
		String[] tokens = { "Hello", "wonderful", "giant", "world", "leader", "!!!", "caca"};
 
		int count = 3;
		Combiner<String> combiner = new Combiner<String>( count, tokens );
		String[] result = new String[count];
		while ( combiner.searchNext( result ) )
			System.out.println( Arrays.toString( result ) );
	}
 
	public static class Combiner<T>
	{
		protected int count;
		protected T[] array;
		protected int[] indexes;
 
		public Combiner( int count, T[] array )
		{
			super();
			this.count = count;
			this.array = array;
			indexes = new int[count];
			for ( int i = 0; i < count; i++ )
				indexes[i] = i;
		}
		
		public int combinatorial() {
			int length = array.length;
			int result = 1;
			for (int i = length; i>length-count; i--) {
				result *= i;
				result /= length-i+1;
			}
			return result;
		}
 
		public boolean searchNext( T[] result )
		{
			if ( indexes == null )
				return false;
 
			int resultIndex = 0;
			for ( int index : indexes )
				result[resultIndex++] = array[index];
 
			int indexesRank = count-1;
			int arrayRank = array.length-1;
			while ( indexes[indexesRank] == arrayRank )
			{
				if ( indexesRank == 0 )
				{
					indexes = null;
					return true;
				}
				indexesRank--;
				arrayRank--;
			}
 
			int restartIndex = indexes[indexesRank] + 1;
			while ( indexesRank < count )
				indexes[indexesRank++] = restartIndex++;
 
			return true;
		}
	}
}