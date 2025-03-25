package pokermax.computer.utils;

public class IteratorSlicer {

    public static int[] getSlice(int processNumber, int totalLength, int numProcesses) {
        int minSliceLength = totalLength / numProcesses;
        int remainder = totalLength % numProcesses;

        int startIndex = processNumber * minSliceLength + Math.min(processNumber, remainder);
        int endIndex = startIndex + minSliceLength + (processNumber < remainder ? 1 : 0);

        return new int[]{startIndex, endIndex};
    }
}