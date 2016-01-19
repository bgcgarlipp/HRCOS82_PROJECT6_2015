/**
 * @author:   John Eatwell
 * @fileName: EmotionsIterator.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.aucomp;

import fer.data.Emotion;
import fer.data.FacsAU;
import java.util.Map;
import java.util.Set;

public abstract class EmotionsIterator
{
    private Map<String, Set<FacsAU>> facs;
    private Map<String, Emotion> emotions;

    protected EmotionsIterator(Map<String, Set<FacsAU>> facs, Map<String, Emotion> emotions)
    {
        this.facs = facs;
        this.emotions = emotions;
    }
    
    public void calculate()
    {
        //Iterate throught each Image
        for (String imageID : facs.keySet())
        {
            // Corresponding AU and emotions
            Set<FacsAU> auSet = facs.get(imageID);
            Emotion emo = emotions.get(imageID);
            
            if (emo != null)
            {
                performCalculation(imageID, emo, auSet);
            }
        }
        performFinalCalculation();
    }
    
    protected abstract void performCalculation(String imageID, Emotion emo, Set<FacsAU> auSet);
    protected void performFinalCalculation() {}
}
