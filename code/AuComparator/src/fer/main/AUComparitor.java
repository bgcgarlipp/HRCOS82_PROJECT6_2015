/**
 * @author:   John Eatwell
 * @fileName: AUComparitor.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.main;

import fer.aucomp.*;
import fer.fileprocessing.*;
import fer.utils.Utils;
import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class AUComparitor
{
    // Label Data
    private final String ckPlusEmotionLabels = "DatabaseLabels/CK_PLUS/Emotion";
    private final String ckPlusFacsLabels = "DatabaseLabels/CK_PLUS/FACS";
    private final String ckEmotionLabels = "DatabaseLabels/CK_EMOTIONS.csv";
    
    //Files to save content (Basic Data Read in)
    private final String ckPlusFacsAUFile = "Output/CKPLUS_FacsAU.txt";
    private final String ckPlusEmotionsFile = "Output/CKPLUS_Emotions.txt";
    private final String ckFacsAUFile = "Output/CK_FacsAU.txt";

            
    private final String EmotionstoAUComplex = "Output/Emo2AU_Complex.txt";
    private final String EmotionstoAUSimple = "Output/Emo2AU_Simple.txt";
    private final String FacsStatsSimple = "Output/FACSStats_Simple.txt";
    private final String FacsStatsComplex = "Output/FACSStats_Complex.txt";
    
    // Running Details
    private AuFileProcessor auProcessor;
    private EmoFileProcessor emoProcessor;
    private CKAuFileProcessor ckProcessor;
    
    // Stats Info
    private AuStatsComplex statsComplex;
    private AuStatsSimple statsSimple;

    public AUComparitor()
    {
        auProcessor = new AuFileProcessor();
        emoProcessor = new EmoFileProcessor();
        ckProcessor = new CKAuFileProcessor();
    }
    
    public void readInDatabases()
    {
        try
        {
            // Read in CK+ FACS AU
            auProcessor.readPath(ckPlusFacsLabels);
            Utils.writeFile(new File(ckPlusFacsAUFile), auProcessor.toString());

            // Read in CK+ Emotions
            emoProcessor.readPath(ckPlusEmotionLabels);
            Utils.writeFile(new File(ckPlusEmotionsFile), emoProcessor.toString());
            
            // Read in CK FACS AU
            ckProcessor.processFile(ckEmotionLabels);
            Utils.writeFile(new File(ckFacsAUFile), ckProcessor.toString());
            
        } catch (IOException ex)
        {
            Logger.getLogger(AUComparitor.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    
    public void processAU()
    {
        // Which Emotions link to AU (Complex)
        AuProcessing process = new AuProcessing(auProcessor.getFacs(), emoProcessor.getEmotions(), false);
        process.calculate();
        Utils.writeFile(new File(EmotionstoAUComplex), process.toString());

        // Which Emotions link to AU (Simple)
        process = new AuProcessing(auProcessor.getFacs(), emoProcessor.getEmotions(), true);
        process.calculate();
        Utils.writeFile(new File(EmotionstoAUSimple), process.toString());

        //Calculate statistics on AAU (Comples)
        AuStatsComplex statsComplex = new AuStatsComplex(auProcessor.getFacs(), emoProcessor.getEmotions());
        statsComplex.calculate();
        Utils.writeFile(new File(FacsStatsComplex), statsComplex.toString());

        //Calculate statistics on AAU (Simple)
        AuStatsSimple statsSimple = new AuStatsSimple(auProcessor.getFacs(), emoProcessor.getEmotions());
        statsSimple.calculate();
        Utils.writeFile(new File(FacsStatsSimple), statsSimple.toString());
        
        System.out.println("Check Output Folder for AU/Emotion Comparisons");
    }
    
    public static void main(String[] args)
    {
        AUComparitor au = new AUComparitor();
        au.readInDatabases();
        
        au.processAU();
    }
}
