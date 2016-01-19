/**
 * @author:   John Eatwell
 * @fileName: CKAuFileProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import fer.data.FacsAU;
import java.io.File;
import java.util.Arrays;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class CKAuFileProcessor extends FileProcessor
{
    private Map<String, Set<FacsAU>> facs;
    
    public CKAuFileProcessor()
    {
        facs = new TreeMap<>();
    }
    
    public void processFile(String ckFileName)
    {
        this.process( (new File(ckFileName)).toPath() );
    }
    
    @Override
    protected void processLine(String fileName, String line)
    {
        if (line.indexOf(',') > 0)
        {
            String [] csv = line.split(",");
            
            // Resolve Image ID (Similar to CK+)
            String imageId = String.format("S%03d_%03d", Integer.parseInt(csv[0]), Integer.parseInt(csv[1]));
            
            // Resolve AU
            String [] auCodes = csv[2].split("\\+");
            Set<FacsAU> auSet = new TreeSet<>();
            for(String auCode : auCodes)
            {
                FacsAU au = FacsAU.resolveCK(auCode);
                auSet.add(au);
            }
            facs.put(imageId, auSet);
        }
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
    
}
