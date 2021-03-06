/**
 *
 * @file    au_detector_cli.cpp (originally emo_detector_cli.cpp)
 * @author  Daniele Bellavista (Emotime)
 * @date    12/27/2013 12:18:32 PM
 * @brief
 *
 * @details Modified By John Eatwell (35264926) as a general SVN classifier
 *
 */

#include "SVMGenDetector.h"
#include "BoostGenDetector.h"
#include "matrix_io.h"
#include "FacePreProcessor.h"
#include "TrainingParameters.h"

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <map>
#include <iostream>
#include <cstddef>         // std::size_t

using namespace cv;
using namespace emotime;

using std::cout;
using std::endl;
using std::cerr;
using std::string;
using std::pair;

/**
 *  @brief          Prints the CLI banner
 *
 */
void banner();

/**
 *  @brief          Prints the CLI help
 *
 */
void help();

void help()
{
	cout << "Usage:" << endl;
	cout << "   emo_detector_cli (svm|ada) <FaceDetecXML> (<EyeDetecXML>|none) <width> <height> <nwidths> <nlambdas> <nthetas> <svmXML> {<svmXML>}" << endl;
	cout << "Parameters:" << endl;
	cout << "   (svm|ada)       - Use ada or svm" << endl;
	cout << "   <FaceDetectXML>   - OpenCV cascade classifier configuration file (Haar or LBP) for face detection" << endl;
	cout << "   <EyeDetectXML>   - OpenCV cascade classifier configuration file (Haar or LBP) for eye detection. If the file is 'none', no eye correction is performed." << endl;
	cout << "   <width>       - Width of the image, the input image will be scaled" << endl;
	cout << "   <height>      - Height of the image, the input image will be scaled" << endl;
	cout << "   <nwidths>     - " << endl;
	cout << "   <nlambdas>    - " << endl;
	cout << "   <nthetas>     - " << endl;
	cout << "   <svmXML>    - The trained svm for detecting an expression " << endl;
	cout << "                   Name format: emotion1_emotion2_..._vs_emotion... where emotion* is one of (neutral, contempt, disgust, fear, sadness, surprise)" << endl;
	cout << endl;
}

void banner()
{
	cout << "EmoDetector Utility:" << endl;
	cout << "     Detect emotions using trained classificator" << endl;
}

/**
 *  @brief          Main
 *
 *  @param[in]      argc
 *  @param[in]     argv
 *
 *  @returns  1
 *
 */
int main(int argc, const char *argv[])
{
	if (argc < 9)
	{
		banner();
		help();
		cerr << "ERR: missing parameters" << endl;
		return -3;
	}
	string infile; // = string(argv[1]);
	string method(argv[1]);
	string config(argv[2]);
	string config_e(argv[3]);

	cv::Size size(0, 0);
	int nwidths, nlambdas, nthetas;
	size.width = abs(atoi(argv[4]));
	size.height = abs(atoi(argv[5]));
	nwidths = abs(atoi(argv[6]));
	nlambdas = abs(atoi(argv[7]));
	nthetas = abs(atoi(argv[8]));
	vector<string> classifier_paths;

	if (argc >= 10)
	{
		// Read boost XML paths
		for (int i = 9; i < argc; i++)
		{
			string clpath(argv[i]);
			classifier_paths.push_back(string(argv[i]));
		}
	}
	else
	{
		cerr << "ERR: you must specify some classifiers" << endl;
		return -2;
	}

	FacePreProcessor* preprocessor;
	GenDetector* gendetector;

	try
	{

		if (config_e == "none")
		{
			preprocessor = new FacePreProcessor(config, size.width, size.height, nwidths, nlambdas, nthetas);
		}
		else
		{
			preprocessor = new FacePreProcessor(config, config_e, size.width, size.height, nwidths, nlambdas, nthetas);
		}

		if (method == "svm")
		{
			gendetector = new SVMGenDetector(kCfactor, kMaxIteration, kErrorMargin);
		}
		else
		{
			gendetector = new BoostGenDetector(kBoostType, kTrimWeight, kMaxDepth);
		}

		gendetector->init(classifier_paths);

		cout << "Insert the image file path: " << endl;
		while (std::getline(std::cin, infile))
		{
			try
			{
				Mat img = matrix_io_load(infile);
				Mat features;
				bool canPreprocess = preprocessor->preprocess(img, features);
				if (!canPreprocess)
				{
					cerr << "ERR: Cannot preprocess this image '" << infile << "'" << endl;
					continue;
				}

				// Predict features based on parsed features
				ConfusionMatrix* confMatrix = gendetector->predict(features);

				cout << "Input File: " << matrix_io_fileName(infile) << " Predicted Values: ";
				int count = 0;
				map<string, int>::iterator it;
				for ( it = confMatrix->classifications.begin(); it != confMatrix->classifications.end(); it++ )
				{
					if (count > 0)
						cout << ",";
					cout << it->first << ":" << it->second;
					count++;
				}
				cout << " Finished Prediction"<< endl;

				cout << "Insert the image file path: " << endl;
			} catch (int ee)
			{
				cerr << "ERR: Something wrong with '" << infile << "' (" << ee << ")" << endl;
			}
		}

		delete gendetector;
		delete preprocessor;
	} catch (int e)
	{
		cerr << "ERR: Exception #" << e << endl;
		return -e;
	}

	return 0;
}
