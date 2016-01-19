/**
 *
 * @file    matrix_io.cpp
 * @author  Daniele Bellavista (Emotime) 
 * @brief   Implementation of matrix_io.h utils
 *
 */

#include "matrix_io.h"
#include <iostream>
#include <fstream>
#include <algorithm>

using namespace std;
using namespace cv;

std::string matrix_io_fileExt( std::string & file)
{
    return file.substr(file.find_last_of(".") + 1);
}

/**
 * Used to extract File Name
 */
std::string matrix_io_fileName( std::string & file)
{
    int nameBegin=std::max( (int) file.find_last_of(string(PATH_SEPARATOR))+1, 0 );
    size_t nameEnd=file.find_last_of(".");
    size_t extLen= file.substr(nameEnd, file.length()-nameEnd).length();
    return file.substr( std::max( (int) file.find_last_of(string(PATH_SEPARATOR))+1, 0 ) , file.length()-nameBegin-extLen );
}

std::string matrix_io_fileBaseName(std::string & file)
{
    int nameBegin=std::max( (int) file.find_last_of(string(PATH_SEPARATOR))+1, 0 );
    return file.substr(nameBegin, string::npos);
}

std::string matrix_io_parent_folder(std::string & file)
{
	int folderEnd = std::max( (int) file.find_last_of(string(PATH_SEPARATOR))+1, 0 );
	std::string fileFolder = file.substr(0, folderEnd - 1);
	int folderBegin = fileFolder.find_last_of(PATH_SEPARATOR);

	return file.substr((folderBegin + 1), (folderEnd - folderBegin - 2) );
}

std::string matrix_io_parent_and_file(std::string & file)
{
	int folderEnd = std::max( (int) file.find_last_of(string(PATH_SEPARATOR))+1, 0 );
	std::string fileFolder = file.substr(0, folderEnd - 1);
	int folderBegin = fileFolder.find_last_of(PATH_SEPARATOR);

	return file.substr( (folderBegin + 1));
}

// Reference: http://stackoverflow.com/questions/236129/split-a-string-in-c
std::vector<std::string> split(const std::string &text, std::string seperator)
{
	  std::vector<std::string> tokens;
	  int start = 0, end = 0;
	  while ((end = text.find(seperator, start)) != std::string::npos) {
	    tokens.push_back(text.substr(start, end - start));
	    start = end + 1;
	  }
	  tokens.push_back(text.substr(start));
	  return tokens;
}

cv::Mat matrix_io_load(std::string & filePath)
{
    try
    {
        string file = filePath;
        string format =  matrix_io_fileExt(file);
        if(format==XMLEXT || format==YMLEXT)
        {
            string name = matrix_io_fileName(file);
            FileStorage fs(file, FileStorage::READ);
            Mat * mat = new Mat();
            fs[name] >> *mat;
            fs.release();
            return *mat;
        }
        else
        {
            // Otherwise threat it as image
            return imread( filePath, CV_LOAD_IMAGE_GRAYSCALE );
        }
    }
    catch (int e)
    {
        cerr<<"ERR: Exception #" << e << endl;
        return *(new Mat(0,0,CV_32FC1));
    }

}

bool matrix_io_save( cv::Mat & mat, std::string & filePath)
{
    try
    {
        string file = filePath;
        string format =  matrix_io_fileExt(file);
        if(format==XMLEXT || format==YMLEXT)
        {
            string name = matrix_io_fileName(file);
            FileStorage fs(file, FileStorage::WRITE);
            fs << name << mat;
            fs.release();
        }
        else
        {
            // Otherwise threat it as image
            if (mat.type()==CV_32FC1)
            {
                double min;
                double max;
                cv::minMaxIdx(mat, &min, &max);
                cv::Mat adjMap;
                cv::convertScaleAbs(mat, adjMap, 255/max);
                imwrite(file, adjMap);
            }
            else
            {
                imwrite(file, mat);
            }
        }
        return true;
    }
    catch (int e)
    {
        cerr<<"ERR: Exception #" << e << endl;
        return false;
    }

}
