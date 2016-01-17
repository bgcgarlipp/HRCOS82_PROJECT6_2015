/**
 *
 * @file    BoostGenDetector.cpp
 * @author  Daniele Bellavista
 * @date    12/27/2013 12:18:32 PM
 *
 */
#include "BoostGenDetector.h"
#include "AdaBoostClassifier.h"

namespace emotime
{

	BoostGenDetector::BoostGenDetector(int boost_type, double trim_weight, int max_depth) :
			GenDetector()
	{
		this->boost_type = boost_type;
		this->trim_weight = trim_weight;
		this->max_depth = max_depth;
	}

	BoostGenDetector::BoostGenDetector(int boost_type, double trim_weight, int max_depth, std::map<std::string, std::pair<vector<std::string>, Classifier*> > detmap_ext) :
			GenDetector(detmap_ext)
	{
		this->boost_type = boost_type;
		this->trim_weight = trim_weight;
		this->max_depth = max_depth;
	}

	Classifier* BoostGenDetector::createClassifier()
	{
		return new AdaBoostClassifier(this->boost_type, this->trim_weight, this->max_depth);
	}

	ConfusionMatrix* BoostGenDetector::predict(cv::Mat& frame)
	{
		return GenDetector::predictOneVsAll(frame);
	}
}
