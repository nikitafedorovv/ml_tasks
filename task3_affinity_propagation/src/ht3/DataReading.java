package ht3;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class DataReading {
    final private static int count = 196591;

    public static Map.Entry<double[][], int[][]> readFile(String path) {

        Random random = new Random();

        double[][] result = new double[count][];
        int[][] indices = new int[count][];

        try {
            FileInputStream fstream = new FileInputStream(path);
            BufferedReader reader = new BufferedReader(new InputStreamReader(fstream));
            String strLine;
            String[] linesplit;
            Integer Vertex = 0;
            LinkedList<Integer> list = new LinkedList<>();
            list.add(Vertex);

            while ((strLine = reader.readLine()) != null) {

                linesplit = strLine.split("\t");

                if (Integer.parseInt(linesplit[0]) != Vertex) {
                    indices[Vertex] = new int[list.size()];
                    result[Vertex] = new double[list.size()];
                    result[Vertex][0] = Clusterization.selfSimilarity;
                    indices[Vertex][0] = Vertex;
                    for (int i = 1; i < result[Vertex].length; i++) {
                        result[Vertex][i] = (random.nextGaussian() + 5) * 0.0001 + 1;
                        indices[Vertex][i] = list.get(i);
                    }

                    Vertex = Integer.parseInt(linesplit[0]);
                    list = new LinkedList<>();
                    list.add(Vertex);
                    list.add(Integer.parseInt(linesplit[1]));
                } else {
                    list.add(Integer.parseInt(linesplit[1]));
                }
            }

            indices[Vertex] = new int[list.size()];
            result[Vertex] = new double[list.size()];
            result[Vertex][0] = -1.0;
            indices[Vertex][0] = Vertex;
            for (int i = 1; i < result[Vertex].length; i++) {
                result[Vertex][i] = (random.nextGaussian() + 5) * 0.0001 + 1;
                indices[Vertex][i] = list.get(i);
            }
        } catch (IOException e) {
            System.out.println("can't read file");
        }

        return new AbstractMap.SimpleEntry<>(result, indices);
    }

    public static ArrayList<Integer>[] readCheckinsFile(String path) {

        ArrayList<Integer>[] result = new ArrayList[count];

        try {
            FileInputStream fstream = new FileInputStream(path);
            BufferedReader reader = new BufferedReader(new InputStreamReader(fstream));
            String strLine;
            String[] linesplit;
            Integer vertex = 0;
            ArrayList<Integer> set = new ArrayList<>();
            set.add(vertex);

            while ((strLine = reader.readLine()) != null) {

                linesplit = strLine.split("\t");

                if (Integer.parseInt(linesplit[0]) != vertex) {
                    result[vertex] = set;
                    set = new ArrayList<>();
                    vertex = Integer.parseInt(linesplit[0]);
                    set.add(Integer.parseInt(linesplit[4]));
                } else {
                    set.add(Integer.parseInt(linesplit[4]));
                }
            }

            result[vertex] = set;
        } catch (IOException e) {
            System.out.println("can't read file");
        }

        return result;
    }

    public static int[] readLabelsFile(String path) {

        int[] result = new int[count];
        int i = 0;

        try {
            FileInputStream fstream = new FileInputStream(path);
            BufferedReader reader = new BufferedReader(new InputStreamReader(fstream));
            String strLine;

            while ((strLine = reader.readLine()) != null) {
                result[i] = Integer.parseInt(strLine);

                i++;
            }
        } catch (IOException e) {
            System.out.println("can't read file");
        }

        return result;
    }
}
