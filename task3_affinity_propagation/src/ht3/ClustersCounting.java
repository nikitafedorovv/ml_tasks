package ht3;

import java.io.FileWriter;
import java.util.*;

public class ClustersCounting {
    static void count(int[] L) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int i = 0; i < L.length; i++) {
            if (count.containsKey(L[i])) {
                count.put(L[i], count.get(L[i]) + 1);
            } else {
                count.put(L[i], 1);
            }
        }

        List<Map.Entry<Integer, Integer>> list = new ArrayList(count.entrySet());
        Collections.sort(list, (a, b) -> (b.getValue()).compareTo(a.getValue()));

        int[] counts = new int[10000];
        for (int j = 0; j < list.size(); j++) {
            if (list.get(j) != null) {
                counts[list.get(j).getValue()]++;
            }
        }

        try {
            FileWriter writer = new FileWriter("resClasses");
            for (int i = 9999; i >= 0; i--) {
                if (counts[i] != 0)
                    writer.write(counts[i] + " cluster(s) with " + i + " object(s)\n");
            }
            writer.close();
        } catch (Exception ex) {
            System.out.println("can't write to file");
        }
    }
}
