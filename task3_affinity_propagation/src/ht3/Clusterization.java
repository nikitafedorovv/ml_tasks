package ht3;

import java.io.FileWriter;
import java.util.AbstractMap;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;

public class Clusterization {

    private double[][] R;
    private double[][] Rtransposed;
    private double[][] A;
    private double[][] S;
    private int[][] I;
    private static int count = 196591;

    private static final int amountOfIterations = 50;
    private static final double parameter = 0.3;
    public static final double selfSimilarity = -1;

    public Clusterization(double[][] S, int[][] I) {
        this.S = S;
        this.A = firstFill(S);
        this.R = firstFill(S);
        this.I = I;
        this.Rtransposed = firstFill(S);
    }

    public void go() {
        int[] labels = new int[count];
        int[] labelsBefore = new int[count];
        int theSameCounter = 0;
        int numberOfClusters = 0;
        for (int iterationNumber = 0; iterationNumber < amountOfIterations; iterationNumber++) {

            if ((iterationNumber + 1) % 10 == 0) {
                System.out.println("iteration " + (iterationNumber + 1));
            }

            // R
            for (int i = 0; i < count; i++) {
                if (S[i].length > 1) {
                    Map.Entry<Integer, Double> max1 = getFirstMaxR(A[i], S[i]);
                    Map.Entry<Integer, Double> max2 = getSecondMaxR(A[i], S[i]);
                    for (int j = 0; j < S[i].length; j++) {
                        if (j != max1.getKey()) {
                            R[i][j] = R[i][j] * (1 - parameter) + parameter * (S[i][j] - max1.getValue());
                            Rtransposed[I[i][j]][getIndex(I[i][j], i)] = Rtransposed[I[i][j]][getIndex(I[i][j], i)] * (1 - parameter) + (parameter) * (S[i][j] - max1.getValue());

                        } else {
                            R[i][j] = R[i][j] * (1 - parameter) + parameter * (S[i][j] - max1.getValue());
                            Rtransposed[I[i][j]][getIndex(I[i][j], i)] = Rtransposed[I[i][j]][getIndex(I[i][j], i)] * (1 - parameter) + (parameter) * (S[i][j] - max2.getValue());
                        }
                    }
                }
            }

            // A
            double[] sumofmaxes = sumOfMaxes(Rtransposed);

            for (int i = 0; i < A.length; i++) {
                A[i][0] = A[i][0] * (1 - parameter) + parameter * (sumofmaxes[i]);
            }

            for (int i = 0; i < A.length; i++) {
                for (int k = 1; k < A[i].length; k++) {
                    double sum = sumofmaxes[I[i][k]];
                    sum -= R[i][k];
                    sum += R[I[i][k]][0];

                    if (sum > 0) {
                        A[i][k] = A[i][k] * (1 - parameter);
                    } else {
                        A[i][k] = A[i][k] * (1 - parameter) + parameter * sum;
                    }
                }
            }

            labels = new int[count];
            HashSet<Integer> hashSet = new HashSet<>();
            for (int i = 0; i < count; i++) {
                int maxIndex = 0;
                double max = -1000;
                for (int k = 0; k < A[i].length; k++) {
                    if (A[i][k] + R[i][k] > max) {
                        max = A[i][k] + R[i][k];
                        maxIndex = I[i][k];
                    }
                }
                labels[i] = maxIndex;
                hashSet.add(maxIndex);
            }

            numberOfClusters = hashSet.size();

            boolean theSame = Arrays.equals(labels, labelsBefore);

            if (theSame) {
                theSameCounter++;
            } else {
                theSameCounter = 0;
            }

//            System.out.println("theSameCounter = " + theSameCounter);

            if (theSameCounter == 10) {
                System.out.println("reached stop condition");
                break;
            }

            labelsBefore = labels;
        }

        System.out.println("number of clusters = " + numberOfClusters);

        try {
            FileWriter writer = new FileWriter("labels.txt");
            for (int i = 0; i < count; i++) {
                writer.write(labels[i] + "\n");
            }
            writer.close();
        } catch (Exception ex) {
            System.out.println("can't write to file");
        }
    }

    public Map.Entry<Integer, Double> getFirstMaxR(double[] aEdges, double[] sEdges) {
        double max = -100.0;
        int index = 0;

        for (int i = 0; i < sEdges.length; i++) {
            if (max < sEdges[i] + aEdges[i]) {
                max = sEdges[i] + aEdges[i];
                index = i;
            }
        }

        return new AbstractMap.SimpleEntry<>(index, max);
    }

    public Map.Entry<Integer, Double> getSecondMaxR(double[] aEdges, double[] sEdges) {
        double max1 = -100.0;
        double max2 = -100.0;
        int index1 = 0;
        int index2 = 0;

        for (int i = 0; i < aEdges.length; i++) {
            if (max1 < sEdges[i] + aEdges[i]) {
                index2 = index1;
                max2 = max1;
                index1 = i;
                max1 = sEdges[i] + aEdges[i];
            } else {
                if (max2 < sEdges[i] + aEdges[i]) {
                    index2 = i;
                    max2 = sEdges[i] + aEdges[i];
                }
            }
        }
        return new AbstractMap.SimpleEntry<>(index2, max2);
    }

    private double[][] firstFill(double[][] S) {

        double[][] M = new double[S.length][];

        for (int i = 0; i < S.length; i++) {
            M[i] = new double[S[i].length];
            for (int j = 0; j < S[i].length; j++) {
                M[i][j] = 0.0;
            }
        }
        return M;
    }

    private double[] sumOfMaxes(double[][] R) {
        double[] sums = new double[R.length];
        for (int i = 0; i < R.length; i++) {
            for (int j = 0; j < R[i].length; j++) {
                if (i != j && (R[i][j] > 0))
                    sums[i] += R[i][j];
            }
        }
        return sums;
    }

    private int getIndex(int row, int id) {
        for (int i = 0; i < I[row].length; i++) {
            if (I[row][i] == id)
                return i;
        }
        return -1;
    }
}
