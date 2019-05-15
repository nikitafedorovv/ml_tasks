package ht3;

import java.util.ArrayList;
import java.util.Map;

public class Main {

    static String path = "loc-gowalla_edges.txt";

    static String pathCheckins = "loc-gowalla_totalCheckins.txt";
    static String pathLabels = "labels.txt";

    public static void main(String[] args) {
        Map.Entry<double[][], int[][]> SI = DataReading.readFile(path);
        double[][] S = SI.getKey();
        int[][] I = SI.getValue();
        Clusterization clusterization = new Clusterization(S, I);
        clusterization.go();

        ArrayList<Integer>[] C = DataReading.readCheckinsFile(pathCheckins);
        int[] L = DataReading.readLabelsFile(pathLabels);
        ClustersCounting.count(L);
        AccuracyCounting.count(L, C);
    }
}
