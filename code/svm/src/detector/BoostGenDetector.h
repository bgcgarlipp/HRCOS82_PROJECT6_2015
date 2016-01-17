/**
 *
 * @file    BoostEmoDetector.h
 * @date    02/08/2014 11:47:13 AM
 * @brief   Definition of BoostEmoDetector
 *
 */

#ifndef _H_BOST_EMO_DETECTOR
#define _H_BOST_EMO_DETECTOR

#include "GenDetector.h"

namespace emotime{

  /**
   * @class    BoostEmoDetector
   *
   * @date    12/27/2013 11:59:26 AM
   *
   * @brief   FacsAU detector specialization using AdaBoost
   *
   */
  class BoostGenDetector : public GenDetector {
    public:


      /**
       *  @brief          Initialize the emodetector with boost parameters and
       *                  empty classifiers.
       *
       *  @param[in]      boost_type Type of the opencv boosting algorithm
       *  @param[in]      trim_weight The opencv trim weight value
       *  @param[in]      max_depth Algorithm max depth
       *
       *  @see AdaBoostClassifier
       *
       */
	  BoostGenDetector(int boost_type, double trim_weight, int max_depth);

      /**
       *  @brief          Initialize the emodetector with boost parameters and
       *                  classifiers.
       *
       *  @param[in]      boost_type Type of the opencv boosting algorithm
       *  @param[in]      trim_weight The opencv trim weight value
       *  @param[in]      max_depth Algorithm max depth
       *  @param[in]      detmap_ext Mapping between emotions and classifier.
       *
       *  @see AdaBoostClassifier
       *
       */
	  BoostGenDetector(int boost_type, double trim_weight, int max_depth, map<string, pair<vector<string>, Classifier*> > detmap_ext);

	  ConfusionMatrix* predict(cv::Mat& frame);

    protected:

      Classifier* createClassifier();

    private:

      /// Type of the opencv boosting algorithm
      int boost_type;
      /// The opencv trim weight value
      double trim_weight;
      /// Algorithm max depth
      int max_depth;
  };

}

#endif
