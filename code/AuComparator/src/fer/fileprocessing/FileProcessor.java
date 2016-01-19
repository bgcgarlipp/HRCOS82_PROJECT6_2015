/**
 * @author:   John Eatwell
 * @fileName: FileProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author John Eatwell
 */
public abstract class FileProcessor implements IFileProcessor
{
    
    @Override
    public void process(Path path)
    {
        String fileName = path.getFileName().toString();
        
        try( BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream( path.toFile() ), StandardCharsets.UTF_8) ))
        {
            String line;
            while((line = br.readLine()) != null)
            {
                if (line.trim().length() > 0) processLine(fileName, line);
            }
        } catch (IOException ex)
        {
            Logger.getLogger(FilePathProcessor.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    protected abstract void processLine(String fileID, String line);
}
