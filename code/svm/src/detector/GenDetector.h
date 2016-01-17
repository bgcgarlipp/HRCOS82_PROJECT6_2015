/**
 *
 * @file    GeneralDetector.h
 * @author  Daniele Bellavista (Emotime)
 * @date    12/27/2013 12:18:32 PM
 *
 */
#ifndef SRC_DETECTOR_GENDETECTOR_H_
#define SRC_DETECTOR_GENDETECTOR_H_

#include "matrix_io.h"
#include "string_utils.h"

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <utility>
#include <limits>

#include <opencv2/opencv.hpp>
#include "Classifier.h"
#include "ConfusionMatrix.h"

using namespace cv;
using namespace std;

namespace emotime {


  /**
   * @brief Retrieve the string associated with an emotion
   *
   * @param[in] emo The enum value
   *
   * @return  A string representation
   */
//  string auStrings(FacsAU au);

  /**
   * @class   EmoDetector
   *
   * @brief   Generic class for performing multi-class classification using
   *          binary classifiers.
   *
   * @details
   *
   */
  class GenDetector {

    public:

	  GenDetector();

      /**
       *  @brief          Initialize the detectors in extended mode (one detector multiple emotion)
       *
       *  @param[in]      detmap_ext A map to name -> (vector<emotion>, detector)
       *
       */
	  GenDetector(std::map<std::string, std::pair<std::vector<string>, Classifier*> >& detmap_ext);
      /**
       *  @brief          Initialize the detector from classifier paths
       *
       *  @param[in]      classifiers_path  Path of various classifier files.
       *
       *  @details        Path must be in the format: emop1_emop2_emopn_vs_emon1_emon2_emonm.xml
       *                  Where emop* is the emotion recognized and emon* is the emotion not recognized.
       *
       */
      void init(vector<std::string>& classifiers_path);

      /**
       * Release an EmoDetector
       */
      virtual ~GenDetector();

      /**
       * Return true if the given emotion is present
       *
       * @param[in]  name  The name to search
       *
       * @return true if the given emotion is present
       *
       */
      bool contains(std::string& name);

      /**
       *  @brief          Predict the Class using using trained classifiers
       *
       *  @param[in]      frame The image to predict
       *
       *  @return         The prediction and its result
       *
       *  @details
       */
      ConfusionMatrix* predictOneVsAll(cv::Mat& frame);

      /**
       * @brief Apply the default prediction method
       *
       * @param[in] frame The image to predict
       *
       * @return The predicted emotion
       */
      virtual ConfusionMatrix* predict(cv::Mat& frame);

      static const std::string UNKNOWN;

    protected:

      /**
       *  @brief          Instantiate a classifier
       *
       *  @return         A new classifier
       *
       */
      virtual Classifier* createClassifier() = 0;

    private:



      /// Detectors for generic approaches (each detector matches one or more emotion)
      map<std::string, std::pair<std::vector<std::string>, Classifier*> > detectors_ext;

      /**
       *  @brief          Initialize the detectors in extended mode (one detector multiple emotion)
       *
       *  @param[in]      detmap_ext A map to name -> (vector<emotion>, detector)
       *
       */
      void init(const std::map<std::string, std::pair<std::vector<std::string>, Classifier*> >& detmap_ext);

  }; // end of EmoDetector
}

#endif /* SRC_DETECTOR_GENDETECTOR_H_ */
