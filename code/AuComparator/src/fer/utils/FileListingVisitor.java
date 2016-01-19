/**
 * @author:   John Eatwell
 * @fileName: FileListingVisitor.java
 * @details:  Code used to compare AU and Emotions
 */
 package fer.utils;

import fer.fileprocessing.IFileProcessor;
import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

public final class FileListingVisitor
{
    private String path;
    private IFileProcessor processor;
    
    
    public FileListingVisitor(IFileProcessor processor, String path)
    {
        this.processor = processor;
        this.path = path;
    }
    
    public void processFiles() throws IOException
    {
        FileVisitor<Path> fileProcessor = new SimpleFileVisitor<Path>()
        {
            @Override
            public FileVisitResult visitFile(Path aFile, BasicFileAttributes aAttrs) throws IOException
            {
                processor.process(aFile);
                return FileVisitResult.CONTINUE;
            }
        };
        
        Files.walkFileTree(Paths.get(path), fileProcessor);
    }
}
