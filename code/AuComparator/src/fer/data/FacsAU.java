/**
 * @author:   John Eatwell
 * @fileName: FacsAU.java
 * @details:  Code used to compare AU and Emotions
 */
package fer.data;

import fer.utils.Utils;
import java.util.List;
import java.util.Objects;

public class FacsAU implements Comparable<FacsAU>
{

    @Override
    public int compareTo(FacsAU o)
    {
        if (this.AU != o.AU)
        {
            return this.AU - o.getAU();
        } else
        {
            return this.intensity.toString().compareToIgnoreCase(o.getIntensity().toString());
        }
    }

    @Override
    public boolean equals(Object obj)
    {
        if (obj == null || obj instanceof FacsAU)
        {
            return false;
        } else
        {
            return compareTo((FacsAU) obj) == 0;
        }
    }

    @Override
    public int hashCode()
    {
        int hash = 7;
        hash = 71 * hash + this.AU;
        hash = 71 * hash + Objects.hashCode(this.intensity);
        return hash;
    }

    public static enum Intensity
    {

        UnRated,
        Trace, // A
        Slight, // B   
        Pronounced, // C
        Severe, // D
        Extreme;     // E

        @Override
        public String toString()
        {
            switch (this)
            {
                case Trace:
                    return "A";
                case Slight:
                    return "B";
                case Pronounced:
                    return "C";
                case Severe:
                    return "D";
                case Extreme:
                    return "E";
            }
            return "";
        }
        
        public static Intensity fromLetter(char c)
        {
            switch(c)
            {
                case 'A':
                    return Intensity.Trace;
                case 'B':
                    return Intensity.Slight;
                case 'C':
                    return Intensity.Pronounced;
                case 'D':
                    return Intensity.Severe;
                case 'E':
                    return Intensity.Extreme;                    
            }
            return Intensity.UnRated;
        }
    }

    private int AU;
    private Intensity intensity = Intensity.UnRated;

    public int getAU()
    {
        return AU;
    }

    public Intensity getIntensity()
    {
        return intensity;
    }

    /*
     AU Number       Intensity (A-E)
     9.0000000e+00   4.0000000e+00
     */
    public static FacsAU resolveCKPlus(String facsLine)
    {
        List<String> data = Utils.extractCKLineData(facsLine);
        FacsAU result = new FacsAU();
        for (int i = 0; i < data.size(); i++)
        {
            if (i == 0)
            {
                result.AU = Double.valueOf(data.get(i)).intValue();
            } else if (i == 1)
            {
                result.intensity = Intensity.values()[Double.valueOf(data.get(i)).intValue()];
            }
        }

        return result;
    }

    public static FacsAU resolveCK(String auDetails)
    {
        
        if (!Utils.isFirstCharDigit(auDetails))
        {
            auDetails = auDetails.substring(1);
        }

        FacsAU result = new FacsAU();
        if (Utils.isLastCharDigit(auDetails))
        {
            result.AU = Integer.parseInt(auDetails);
        } else
        {
            auDetails = auDetails.toUpperCase();
            result.AU = Integer.parseInt(auDetails.substring(0, auDetails.length() - 1));
            result.intensity = Intensity.fromLetter( auDetails.charAt(auDetails.length() - 1));
        }

        return result;
    }

    @Override
    public String toString()
    {
        return String.format("%d%s", AU, intensity.toString());
    }

}
