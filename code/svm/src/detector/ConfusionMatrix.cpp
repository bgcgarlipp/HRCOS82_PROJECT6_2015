/**
 *
 * @file    ConfusionMatrix.cpp
 * @author  John Eatwell (35264926)
 * @date    28/11/2015
 * @brief   Originally created to extract Confusion matrix while predicted 
 *          it was later decided to perform these calculations in the python code
 *          Classoifications are provided via au_detector_cli and provided to python (performVerification.py)
 *
 */
#include "ConfusionMatrix.h"

using namespace std;

namespace emotime
{
	
	ConfusionMatrix::ConfusionMatrix() { }
	
	ConfusionMatrix::~ConfusionMatrix()
	{
		// Cleanup parsed Classifications
		for(std::map<std::string, int>::iterator itr = classifications.begin(); itr != classifications.end(); itr++)
		{
			classifications.erase(itr);
		}		
	}

}
