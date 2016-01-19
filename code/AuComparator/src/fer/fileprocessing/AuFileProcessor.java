/**
 * @author:   John Eatwell
 * @fileName: AuFileProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import fer.data.FacsAU;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class AuFileProcessor extends FilePathProcessor
{

    private Map<String, Set<FacsAU>> facs;
    
    public AuFileProcessor()
    {
        facs = new TreeMap<>();
    }
    
    
    @Override
    public void processLine(String fileName, String line)
    {
        String fileID = fileName.substring(0,8);
        FacsAU au = FacsAU.resolveCKPlus(line);
        if (facs.get(fileID) == null)
            facs.put(fileID, new TreeSet<FacsAU>());
        facs.get(fileID).add(au);
    }
    
    @Override
    public String toString()
    {
        StringBuilder sb = new StringBuilder();
        sb.append("Image    : AU\n");
        sb.append("----------------------------------\n");
        
        for(String imageID : facs.keySet())
        {
            sb.append(imageID).append(" : ");
            int i =0;
            for(FacsAU au : facs.get(imageID))
            {
                sb.append((i++>0)? ", " : "");
                sb.append( au.toString() );
            }
            
            sb.append("\n");
        }
        return sb.toString();
    }

    public Map<String, Set<FacsAU>> getFacs()
    {
        return facs;
    }
    
}
