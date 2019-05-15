package ht3;

import java.util.*;

public class AccuracyCounting {
    static int counterNodes = 196591;
    static int[][] suggestions = new int[196591][10];
    static HashMap<Integer, Integer>[] rating = new HashMap[counterNodes];
    static int numberOfRandoms = 10000;

    public static void count(int[] L, ArrayList<Integer>[] C) {
        HashSet<Integer> randomIDs = getRandoms();
        suggestions = fillSuggestions(counterNodes, 10);

        // Calculating recommendations
        for (int i = 0; i < counterNodes; i++) {
            rating[i] = new HashMap<>();
        }
        rating = recommend(L, C, rating);

        // Sorting suggestions
        for (int i = 0; i < rating.length; i++) {
            List<Map.Entry<Integer, Integer>> list = new ArrayList(rating[i].entrySet());
            Collections.sort(list, (a, b) -> (b.getValue()).compareTo(a.getValue()));
            for (int j = 0; j < (list.size() < 10 ? list.size() : 10); j++) {
                if (list.get(j) != null) {
                    suggestions[i][j] = list.get(j).getKey();
                }
            }
        }

        // Suggesting count-ins to users
        double correct = 0.0;
        int all = 0;
        for (Integer i : randomIDs) {
            for (int j = 0; j < 10; j++) {
                if (C[i] != null) {
                    if ((C[i].contains(suggestions[L[i]][j]))) {
                        correct++;
                    }

                    all++;
                }
            }
        }
        System.out.println("Accuracy = " + (correct / all));
    }

    private static HashMap<Integer, Integer>[] recommend(int[] L, ArrayList<Integer>[] C, HashMap<Integer, Integer>[] rating) {
        for (int i = 0; i < C.length; i++) {
            int clust = L[i];

            if (C[i] != null) {
                for (Integer check : C[i]) {
                    if (rating[clust].containsKey(check)) {
                        rating[clust].put(check, rating[clust].get(check) + 1);
                    } else {
                        rating[clust].put(check, 1);
                    }
                }
            }
        }
        return rating;
    }

    private static HashSet<Integer> getRandoms() {
        HashSet<Integer> randoms = new HashSet<>();
        Random r = new Random();
        while (randoms.size() < numberOfRandoms) {
            randoms.add(r.nextInt(counterNodes));
        }
        return randoms;
    }

    private static int[][] fillSuggestions(int rows, int cols) {
        int[][] result = new int[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = -1;
            }
        }
        return result;
    }
}
