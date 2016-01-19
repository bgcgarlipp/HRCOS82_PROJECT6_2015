/**
 * @author:   John Eatwell
 * @fileName: FilePathProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import fer.utils.FileListingVisitor;
import java.io.IOException;

public abstract class FilePathProcessor extends FileProcessor
{
    public void readPath(String path) throws IOException
    {
        FileListingVisitor visitor = new FileListingVisitor(this, path);
        visitor.processFiles();
    }
                
}
