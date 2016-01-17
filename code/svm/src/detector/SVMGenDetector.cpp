/**
 *
 * @file    SVMGenDetector.cpp
 * @author  Daniele Bellavista (Emotime)
 * @date    12/27/2013 12:18:32 PM
 *
 */
#include "SVMGenDetector.h"
#include "SVMClassifier.h"

namespace emotime
{

	SVMGenDetector::SVMGenDetector(double C_factor, int max_iteration, double error_margin) :
			GenDetector()
	{
		this->C_factor = C_factor;
		this->max_iteration = max_iteration;
		this->error_margin = error_margin;
	}

	SVMGenDetector::SVMGenDetector(double C_factor, int max_iteration, double error_margin, std::map<std::string, std::pair<vector<std::string>, Classifier*> > detmap_ext) :
			GenDetector(detmap_ext)
	{
		this->C_factor = C_factor;
		this->max_iteration = max_iteration;
		this->error_margin = error_margin;
	}

	Classifier* SVMGenDetector::createClassifier()
	{
		return new SVMClassifier(this->C_factor, this->max_iteration, this->error_margin);
	}

	ConfusionMatrix* SVMGenDetector::predict(cv::Mat& frame)
	{
		return GenDetector::predictOneVsAll(frame);
	}
}
