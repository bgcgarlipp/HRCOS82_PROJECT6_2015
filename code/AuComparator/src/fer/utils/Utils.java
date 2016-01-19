/**
 * @author:   John Eatwell
 * @fileName: Utils.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.utils;

import fer.data.Emotion;
import fer.data.FacsAU;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Utils
{

    public final static String LINE_SEPERATOR = System.getProperty("line.separator");

    public static List<String> extractCKLineData(String line)
    {
        List<String> result = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        boolean found = false;
        for (int i = 0; i < line.length(); i++)
        {
            if ("0123456789.e+-".indexOf(line.charAt(i)) >= 0)
            {
                sb.append(line.charAt(i));
                found = true;
            } else if (found)
            {
                result.add(sb.toString());
                sb = new StringBuilder();
                found = false;
            }
        }
        if (found)
        {
            result.add(sb.toString());
        }

        return result;
    }

    public static String facsSetToString(Set<FacsAU> facs, boolean simplified)
    {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        for (FacsAU fc : facs)
        {
            sb.append((i++ > 0) ? "," : "");
            sb.append(simplified ? fc.getAU() : fc.toString());
        }
        return sb.toString();
    }

    public static String facsSetToString(Set<FacsAU> facs)
    {
        return facsSetToString(facs, false);
    }

    public static String simplifiedFacsSetToString(Set<FacsAU> facs)
    {
        return facsSetToString(facs, true);
    }

    /*
     Inspired by:
     http://stackoverflow.com/questions/109383/how-to-sort-a-mapkey-value-on-the-values-in-java
     */
    public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map, final boolean smallestToLargest)
    {
        //First Create Sorted List
        List<Map.Entry<K, V>> list = new LinkedList<>(map.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<K, V>>()
        {
            @Override
            public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2)
            {
                if (smallestToLargest)
                {
                    return (o1.getValue()).compareTo(o2.getValue());
                } else
                {
                    return (o2.getValue()).compareTo(o1.getValue());
                }
            }
        });

        // Now Recreate sorted Map
        Map<K, V> result = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list)
        {
            result.put(entry.getKey(), entry.getValue());
        }

        return result;
    }

    public static <K, V> Map<K, V> sortByKey(Map<K, V> map, final boolean smallestToLargest)
    {
        TreeMap<K, V> result = null;

        if (smallestToLargest)
        {
            result = new TreeMap<>();
        } else
        {
            result = new TreeMap<>(Collections.reverseOrder());
        }

        result.putAll(map);

        return result;
    }

    public static void writeFile(File file, String content)
    {
        file.getParentFile().mkdirs();
        
        try (BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8)))
        {
            bw.write(content);
        } catch (IOException ex)
        {
            Logger.getLogger(Utils.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public static String createHeader(Emotion emo)
    {
        StringBuilder sb = new StringBuilder();

        sb.append(String.format("= %s =", emo.toString()));
        int len = sb.length();
        sb.append(LINE_SEPERATOR);

        for (int i = 0; i < len; i++)
        {
            sb.append("-");
        }
        sb.append(LINE_SEPERATOR);

        return sb.toString();
    }

    public static boolean isFirstCharDigit(final String str)
    {
        final char c = str.charAt(0);
        return (c >= '0' && c <= '9');
    }
    
    public static boolean isLastCharDigit(final String str)
    {
        final char c = str.charAt(str.length()-1);
        return (c >= '0' && c <= '9');
    }
            
}
