/**
 * @author:   John Eatwell
 * @fileName: EmotionDefinition.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.data;

import fer.utils.Utils;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

/**
 *
 * @author John Eatwell
 */
public class EmotionDefinition
{
    private boolean simplifiedAU;
    private Emotion emotion;
    private Set<String> imageIDs;
    private Set<FacsAU> facs;

    private String emoString = null;  // Cached version of facs List
    
    public EmotionDefinition(Emotion emotion, boolean simplifiedAU)
    {
        this.emotion = emotion;
        this.imageIDs = new TreeSet<>();
        this.facs = new TreeSet<>();
        this.simplifiedAU = simplifiedAU;
    }
    
    public void refreshFacsCache()
    {
        emoString = Utils.facsSetToString(facs, simplifiedAU);
    }
    
    public String toString()
    {
        StringBuilder sb = new StringBuilder();
        
        int i=0;
        for(String id : imageIDs)
        {
            sb.append((i++>0)? "," : "");
            sb.append( id );
        }
        
        sb.append(" : ");
        i=0;
        for(FacsAU au : facs)
        {
            sb.append((i++>0)? "," : "");
            sb.append( simplifiedAU? au.getAU() : au.toString() );
        }
        
        return sb.toString();
    }

//<editor-fold defaultstate="collapsed" desc="accessors">
    public Emotion getEmotion()
    {
        return emotion;
    }
    
    public void setEmotion(Emotion emotion)
    {
        this.emotion = emotion;
    }
    
    public Set<String> getImageIDs()
    {
        return imageIDs;
    }
    
    public void setImageIDs(Set<String> imageIDs)
    {
        this.imageIDs = imageIDs;
    }
    
    public Set<FacsAU> getFacs()
    {
        return facs;
    }
    
    public void setFacs(Set<FacsAU> facs)
    {
        this.facs = facs;
    }
    
    public String getEmoString()
    {
        if (emoString == null)
            refreshFacsCache();
        return emoString;
    }

    public void setEmoString(String emoString)
    {
        this.emoString = emoString;
    }
//</editor-fold>

    
}
