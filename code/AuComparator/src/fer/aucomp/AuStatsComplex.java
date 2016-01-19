/**
 * @author:   John Eatwell
 * @fileName: AuStatsComplex.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.aucomp;

import fer.data.Emotion;
import fer.data.FacsAU;
import fer.utils.Utils;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class AuStatsComplex extends EmotionsIterator
{

    Map<Emotion, Integer> imagesPerEmotion;
    Map<Emotion, Map<String, Integer>> facsOccurences;   //with Intensities
    Map<Emotion, Map<String, Double>> facsAverageUse;   //with Intensities

    public AuStatsComplex(Map<String, Set<FacsAU>> facs, Map<String, Emotion> emotions)
    {
        super(facs, emotions);
        facsOccurences = new HashMap<>();
        imagesPerEmotion = new HashMap<>();
        facsAverageUse = new HashMap<>();
    }

    @Override
    protected void performCalculation(String imageID, Emotion emo, Set<FacsAU> auSet)
    {
        // Initialize arrays
        if (!imagesPerEmotion.containsKey(emo))
        {
            imagesPerEmotion.put(emo, 0);
            facsOccurences.put(emo, new TreeMap<String, Integer>());
        }

        // Each image is assumed unique and conveys a unique emotion
        imagesPerEmotion.put(emo, imagesPerEmotion.get(emo) + 1);

        for (FacsAU au : auSet)
        {
            String facsLabel = au.toString();
            // Handle intensity (using facsOccurences)
            if (!facsOccurences.get(emo).containsKey(facsLabel))
            {
                facsOccurences.get(emo).put(au.toString(), 1);
            } else
            {
                facsOccurences.get(emo).put(au.toString(), facsOccurences.get(emo).get(facsLabel) + 1);
            }
        }
    }

    @Override
    protected void performFinalCalculation()
    {
        // Finally aggregate and perform calculations
        for (Emotion emo : imagesPerEmotion.keySet())
        {
            facsAverageUse.put(emo, new TreeMap<String, Double>());

            for (String facs : facsOccurences.get(emo).keySet())
            {
                double percentageUse = ((facsOccurences.get(emo).get(facs) * 100) / (double) imagesPerEmotion.get(emo));
                facsAverageUse.get(emo).put(facs, percentageUse);
            }
        }
    }

    @Override
    public String toString()
    {
        StringBuilder sb = new StringBuilder();

        for (Emotion emo : imagesPerEmotion.keySet())
        {
            //Emotion Heading
            sb.append(Utils.createHeader(emo));

            // Stats with Just AU
            for (String au : Utils.sortByValue(facsAverageUse.get(emo), false).keySet())
            {
                sb.append(String.format("%3s : %.2f%n", au, facsAverageUse.get(emo).get(au)));
            }

        }
        return sb.toString();
    }

}
