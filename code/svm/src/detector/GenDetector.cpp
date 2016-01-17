/**
 * @file    GenDetector.cpp
 * @date    orig: 01/10/2014 update: Nov 2015
 * @details Modified by John Eatwell (35264926) for use as a 
 *          general AU and Emotion classifier
 */
#include "matrix_io.h"
#include "string_utils.h"

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <utility>
#include <limits>

#include <opencv2/opencv.hpp>
#include "GenDetector.h"

using std::pair;
using std::map;
using std::string;
using std::vector;
using std::make_pair;

using std::numeric_limits;

using std::cerr;
using std::endl;

using cv::Mat;

namespace emotime
{

	const std::string GenDetector::UNKNOWN = "unknown";

	void GenDetector::init(const std::map<std::string, std::pair<std::vector<std::string>, Classifier*> >& detmap_ext)
	{
		this->detectors_ext = detmap_ext;

		//for(it_type iterator = m.begin(); iterator != m.end(); iterator++) {
		for (map<std::string, std::pair<std::vector<std::string>, Classifier*> >::const_iterator ii = detmap_ext.begin(); ii != detmap_ext.end(); ++ii)
		{
			// iterator -> first == key
			// iterator -> second == value
			vector<string> emv = ii->second.first;
			this->detectors_ext.insert(make_pair(ii->first, make_pair(emv, ii->second.second)));
		}
	}

	GenDetector::GenDetector()
	{
	}

	GenDetector::GenDetector(std::map<std::string, std::pair<std::vector<std::string>, Classifier*> >& detmap_ext)
	{
		init(detmap_ext);
	}

	GenDetector::~GenDetector()
	{
		for (map<string, pair<vector<std::string>, Classifier*> >::const_iterator ii = this->detectors_ext.begin(); ii != this->detectors_ext.end(); ++ii)
		{
			delete ii->second.second;
		}
		detectors_ext.clear();
	}

	void GenDetector::init(std::vector<std::string>& classifier_paths)
	{
		map<std::string, pair<vector<std::string>, Classifier*> > classifiers;

		// path is split by _ so AU0_vs_AU1_AU2 becomes [AU0, AU1, AU2]
		for (size_t i = 0; i < classifier_paths.size(); i++)
		{

			std::string clpath = classifier_paths[i];
			Classifier* cvD = this->createClassifier();
			cvD->load(clpath);

			std::string fname = matrix_io_fileBaseName(clpath);
			std:std::string au = "unknown";

			vector<std::string> generalList = split_string(fname, "_");
			vector<std::string> fin_gen_list;
			fin_gen_list.reserve(generalList.size());
			std::string label = "";

			for (vector<std::string>::iterator it = generalList.begin(); it != generalList.end(); ++it)
			{
				au = *it;
				if (au == "vs")
				{
					break;
				}

				if (label.size() > 0)
				{
					label.append("_");
				}
				label.append(au);
				fin_gen_list.push_back(au);
			}
			pair<vector<std::string>, Classifier*> value(fin_gen_list, cvD);		// Multiple AU will be identified by same classifier
			pair<std::string, pair<vector<std::string>, Classifier*> > entry(label, value);
			classifiers.insert(entry);
		}

		init(classifiers);
	}

	/**
	 * Created for debugging AU purposes
	 */
	void printPrediction(std::string method, std::string ident, float prediction)
	{
		cout << "Prediction(MTD:{" << method << "} Key:[" << ident << "] Pred:[" << prediction << "])\n";
	}

	ConfusionMatrix* GenDetector::predictOneVsAll(cv::Mat& frame)
	{
		ConfusionMatrix* result = new ConfusionMatrix();

		if (detectors_ext.size() > 0)
		{
			for (map<std::string, pair<vector<std::string>, Classifier*> >::iterator ii = this->detectors_ext.begin(); ii != this->detectors_ext.end(); ++ii)
			{
				vector<std::string> predictedClassification = ii->second.first; // detected AU
				Classifier* cl = ii->second.second;
				float prediction = cl->predict(frame);	// 0 -> N, 1 -> P
				for (vector<std::string>::iterator predClass_it = predictedClassification.begin(); predClass_it != predictedClassification.end(); ++predClass_it)
				{
					std::string predClass = *predClass_it;
					result->classifications.insert(make_pair(predClass, prediction));
				}
			}
		}
		return result;
	}

	ConfusionMatrix* GenDetector::predict(cv::Mat& frame)
	{
		return predictOneVsAll(frame);
	}
}
