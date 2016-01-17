/**
 *
 * @file    SVMGenDetector.h
 * @author  Daniele Bellavista (Emotime)
 * @date    12/27/2013 12:18:32 PM
 *
 */
#ifndef SRC_DETECTOR_SVMGENDETECTOR_H_
#define SRC_DETECTOR_SVMGENDETECTOR_H_

#include "GenDetector.h"

namespace emotime
{

	/**
	 * @brief   EmoDetector specialization using SVMClassifier
	 */
	class SVMGenDetector: public GenDetector
	{
		public:

			/**
			 *  @brief          Creates an SVMEmoDetector with svm parameters and
			 *                  empty classifiers.
			 *
			 *  @param[in]      C_factor  The algorithm C factor
			 *  @param[in]      max_iteration Maximum number of iteration termination criteria
			 *  @param[in]      error_margin Minimum error termination criteria
			 *
			 *  @see SVMClassifier
			 */
			SVMGenDetector(double C_factor, int max_iteration, double error_margin);

			/**
			 *  @brief          Creates an SVMEmoDetector with svm parameters and
			 *                  classifiers.
			 *
			 *  @param[in]      C_factor  The algorithm C factor
			 *  @param[in]      max_iteration Maximum number of iteration termination criteria
			 *  @param[in]      error_margin Minimum error termination criteria
			 *  @param[in]      detmap_ext Mapping between emotions and classifier.
			 *
			 *  @see SVMClassifier
			 */
			SVMGenDetector(double C_factor, int max_iteration, double error_margin, std::map<std::string, std::pair<vector<std::string>, Classifier*> > detmap_ext);

			ConfusionMatrix* predict(cv::Mat& frame);

		protected:

			Classifier* createClassifier();

		private:

			/// The algorithm C factor
			double C_factor;
			/// Maximum number of iteration termination criteria
			int max_iteration;
			/// Minimum error termination criteria
			double error_margin;

	};

}

#endif /* SRC_DETECTOR_SVMGENDETECTOR_H_ */
