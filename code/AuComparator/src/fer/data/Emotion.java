/**
 * @author:   John Eatwell
 * @fileName: Emotion.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.data;

import fer.utils.Utils;
import java.util.Comparator;
import java.util.List;

public enum Emotion implements Comparator<Emotion>
{
    Neutral,
    Anger,
    Contempt,
    Disgust,
    Fear,
    Happy,
    Sadness,
    Surprise,
    UNKNOWN;
        
    public static Emotion resolveCKPlus(String facsLine)
    {
        List<String> data = Utils.extractCKLineData(facsLine);
        if (data.size() > 0)
        {
            int emoNum = Double.valueOf( data.get(0) ).intValue();
            return values()[emoNum];
        }
        return UNKNOWN;
    }

    @Override
    public int compare(Emotion o1, Emotion o2)
    {
        return o1.compareTo(o2);
    }

}
