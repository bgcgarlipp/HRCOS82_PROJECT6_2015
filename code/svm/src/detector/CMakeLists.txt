# Location src/detector
# Modified by John Eatwell (35264926)

find_package(OpenCV COMPONENTS opencv_core opencv_ml opencv_imgproc opencv_highgui opencv_objdetect REQUIRED)

add_executable(au_detector_cli au_detector_cli.cpp
                                ConfusionMatrix.h
                                ConfusionMatrix.cpp
                                GenDetector.h
                                GenDetector.cpp
                                BoostGenDetector.h
                                BoostGenDetector.cpp
                                SVMGenDetector.h
                                SVMGenDetector.cpp
                                ../training/FacePreProcessor.h
                                ../training/FacePreProcessor.cpp
                                ../training/Classifier.h
                                ../training/Classifier.cpp
                                ../training/SVMClassifier.h
                                ../training/SVMClassifier.cpp
                                ../training/AdaBoostClassifier.h
                                ../training/AdaBoostClassifier.cpp
                                ../utils/matrix_io.h
                                ../utils/matrix_io.cpp
                                ../gaborbank/GaborBank.h
                                ../gaborbank/GaborBank.cpp
                                ../utils/string_utils.h
                                ../utils/string_utils.cpp
                                ../facedetector/FaceDetector.h
                                ../facedetector/FaceDetector.cpp)

target_link_libraries(au_detector_cli ${OpenCV_LIBS} )

INSTALL(TARGETS au_detector_cli DESTINATION ${ASSETDIR} )
