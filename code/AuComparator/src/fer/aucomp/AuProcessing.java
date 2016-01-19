/**
 * @author:   John Eatwell
 * @fileName: AuProcessing.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.aucomp;

import fer.data.Emotion;
import fer.data.EmotionDefinition;
import fer.data.FacsAU;
import fer.utils.Utils;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class AuProcessing extends EmotionsIterator
{

    private final Map<Emotion, List<EmotionDefinition>> emotionDefintions;
    private boolean simplifyAU = false;

    public AuProcessing(Map<String, Set<FacsAU>> facs, Map<String, Emotion> emotions, boolean simplifyAU)
    {
        super(facs, emotions);
        emotionDefintions = new TreeMap<>();
        this.simplifyAU = simplifyAU;
    }

    @Override
    protected void performCalculation(String imageID, Emotion emo, Set<FacsAU> auSet)
    {
        // Uniquely Identify FACS
        String auSetId = Utils.facsSetToString(auSet, simplifyAU);

        if (emo != null)
        {
            if (emotionDefintions.get(emo) == null)
            {
                emotionDefintions.put(emo, new ArrayList<EmotionDefinition>());
            }

            boolean found = false;
            Iterator<EmotionDefinition> iter = emotionDefintions.get(emo).iterator();
            while (iter.hasNext())
            {
                EmotionDefinition emoDef = iter.next();
                if (emoDef.getEmoString().equals(auSetId))
                {
                    emoDef.getImageIDs().add(imageID);
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                EmotionDefinition emoDef = new EmotionDefinition(emo, simplifyAU);
                emoDef.getFacs().addAll(auSet);
                emoDef.getImageIDs().add(imageID);
                emoDef.refreshFacsCache();
                emotionDefintions.get(emo).add(emoDef);
            }
        }
    }

    @Override
    public String toString()
    {
        StringBuilder sb = new StringBuilder();

        for (Emotion emo : emotionDefintions.keySet())
        {
            sb.append(Utils.createHeader(emo));
            for (EmotionDefinition def : emotionDefintions.get(emo))
            {
                sb.append(def.toString()).append("\n");
            }
            sb.append("\n");
        }
        return sb.toString();
    }

}
