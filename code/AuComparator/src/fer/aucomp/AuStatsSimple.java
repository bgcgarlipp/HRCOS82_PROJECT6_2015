/**
 * @author:   John Eatwell
 * @fileName: AuStatsSimple.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.aucomp;

import fer.data.Emotion;
import fer.data.FacsAU;
import fer.utils.Utils;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 *
 * @author John Eatwell
 */
public class AuStatsSimple extends EmotionsIterator
{
    private Map<Emotion, Integer> imagesPerEmotion;
    private Map<Emotion, Map<Integer, Integer>> auOccurences;    //Ignoring Intensities
    private Map<Emotion, Map<Integer, Double>> auAverageUse;    //Ignoring Intensities

    public AuStatsSimple(Map<String, Set<FacsAU>> facs, Map<String, Emotion> emotions)
    {
        super(facs, emotions);
        auOccurences = new HashMap<>();
        imagesPerEmotion = new HashMap<>();
        auAverageUse = new HashMap<>();
    }

    @Override
    protected void performCalculation(String imageID, Emotion emo, Set<FacsAU> auSet)
    {
        // Initialize arrays
        if (!imagesPerEmotion.containsKey(emo))
        {
            auOccurences.put(emo, new HashMap<Integer, Integer>());
            imagesPerEmotion.put(emo, 0);
        }

        // Each image is assumed unique and conveys a unique emotion
        imagesPerEmotion.put(emo, imagesPerEmotion.get(emo) + 1);

        for (FacsAU au : auSet)
        {
            // auOccurences contains general AU without intensity
            if (!auOccurences.get(emo).containsKey(au.getAU()))
            {
                auOccurences.get(emo).put(au.getAU(), 1);
            } else
            {
                auOccurences.get(emo).put(au.getAU(), auOccurences.get(emo).get(au.getAU()) + 1);
            }

        }
    }
    
    @Override
    protected void performFinalCalculation()
    {
        // Finally aggregate an perform calculations
        for (Emotion emo : imagesPerEmotion.keySet())
        {
            auAverageUse.put(emo, new HashMap<Integer, Double>());

            for (Integer au : auOccurences.get(emo).keySet())
            {
                double percentageUse = ((auOccurences.get(emo).get(au) * 100) / (double) imagesPerEmotion.get(emo));
                auAverageUse.get(emo).put(au, percentageUse);
            }
        }
    }
    
    @Override
    public String toString()
    {
        StringBuilder sb = new StringBuilder();

        for (Emotion emo : auAverageUse.keySet())
        {
            //Emotion Heading
            sb.append(Utils.createHeader(emo));

            // Stats with AU
            for (int au : Utils.sortByValue(auAverageUse.get(emo), false).keySet())
            {
            sb.append(String.format("%2d : %.2f%n", au, auAverageUse.get(emo).get(au)));
        }

        }
        return sb.toString();
    }

}
