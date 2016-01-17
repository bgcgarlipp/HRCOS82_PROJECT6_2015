/**
 *
 * @file    ConfusionMatrix.h
 * @author  John Eatwell (35264926)
 * @date    28/11/2015
 * @brief   Originally created to extract Confusion matrix while predicted 
 *          it was later decided to perform these calculations in the python code
 *          Classoifications are provided via au_detector_cli and provided to python (performVerification.py)
 *
 */

#ifndef SRC_DETECTOR_CONFUSIONMATRIX_H_
#define SRC_DETECTOR_CONFUSIONMATRIX_H_

#include <utility>
#include <string>
#include <map>

namespace emotime
{
	
	class ConfusionMatrix
	{
		public:
			ConfusionMatrix();

			virtual ~ConfusionMatrix();

			// All Classifications
			std::map<std::string, int> classifications;
	};

}

#endif /* SRC_DETECTOR_CONFUSIONMATRIX_H_ */
