/**
 * @author:   John Eatwell
 * @fileName: EmoFileProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import fer.data.Emotion;
import fer.utils.Utils;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class EmoFileProcessor extends FilePathProcessor
{
    private Map<String, Emotion> emotions;
    private Set<Emotion> emotionSet;
    
    public EmoFileProcessor()
    {
        emotions = new TreeMap<>();
        emotionSet = new TreeSet<>();
    }
    
    
    @Override
    public void processLine(String fileName, String line)
    {
        String fileID = fileName.substring(0,8);
        Emotion emo = Emotion.resolveCKPlus(line);
        if (emotions.get(fileID) != null)
            System.err.println("Problem processing EmoFileProcessor: " + fileID);
        emotions.put(fileID, emo);
        emotionSet.add(emo);
    }
    
    @Override
    public String toString()
    {
        StringBuilder sb = new StringBuilder();
        
        for(Emotion emo : emotionSet)
        {
            sb.append(Utils.createHeader(emo));
            for(String imageID: emotions.keySet())
            {
                if (emotions.get(imageID).equals(emo))
                {
                    sb.append(String.format("%s%n", imageID));
                }
            }
            sb.append(Utils.LINE_SEPERATOR);
        }
        
        return sb.toString();
    }

    public Map<String, Emotion> getEmotions()
    {
        return emotions;
    }
    
}
