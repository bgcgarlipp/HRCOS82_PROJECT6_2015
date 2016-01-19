/**
 * @author:   John Eatwell
 * @fileName: IFileProcessor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.fileprocessing;

import java.nio.file.Path;

public interface IFileProcessor
{
    public void process(Path path);
}
